"""
Advanced Fake News Detection System
Enhanced Version with API Key Authentication
Author: Manas Baiswar
Institution: DIT University, Dehradun
"""
import os
import hmac
from functools import wraps
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import logging
from datetime import datetime

from detector import FakeNewsDetector
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Fail fast on insecure production configuration (no-op in debug/dev mode)
try:
    Config.validate()
except RuntimeError as exc:
    logger.error(str(exc))
    raise

# Enable CORS (environment-configurable; defaults to "*" only if CORS_ORIGINS is unset)
CORS(app, resources={r"/api/*": {"origins": Config.get_cors_origins()}})

# Rate limiting (global default now respects the configured API_RATE_LIMIT)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{Config.API_RATE_LIMIT} per hour"]
)

# Initialize detector
detector = FakeNewsDetector()


def require_api_key(f):
    """Decorator for API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            logger.warning(f"API request without key from {get_remote_address()}")
            return jsonify({'error': 'API key required'}), 401
        if not hmac.compare_digest(api_key, app.config['API_KEY']):
            logger.warning(f"Invalid API key attempt from {get_remote_address()}")
            return jsonify({'error': 'Invalid API key'}), 403
        return f(*args, **kwargs)
    return decorated_function


def _perform_analysis(data):
    """
    Shared validation + prediction logic used by both the protected
    external API (/api/analyze) and the same-origin web UI proxy
    (/web/analyze), so the two stay in sync and neither duplicates or
    drifts from the other's rules.

    Returns a (payload_dict, http_status) tuple.
    """
    if not data:
        return {'error': 'No data provided or invalid JSON'}, 400

    input_type = data.get('type', 'text')
    content = data.get('content', '')

    if not content:
        return {'error': 'Content cannot be empty'}, 400

    # Validate input type
    if input_type not in ['text', 'url']:
        return {'error': 'Invalid input type. Use "text" or "url"'}, 400

    # Get text from URL or use direct text
    if input_type == 'url':
        text = detector.scrape_article(content)
        if text.startswith('Error') or text.startswith('Could not'):
            return {'error': text}, 400
    else:
        text = content

    # Validate text length
    if len(text.strip()) < 10:
        return {'error': 'Text too short (minimum 10 characters)'}, 400

    if len(text) > 50000:
        return {'error': 'Text too long (maximum 50,000 characters)'}, 400

    result = detector.predict(text)

    if 'error' in result:
        return result, 503

    logger.info(f"Prediction: {result['prediction']} (Confidence: {result['confidence']}%)")
    # Add metadata
    result['timestamp'] = datetime.utcnow().isoformat()
    result['input_type'] = input_type
    result['text_length'] = len(text)

    return result, 200


@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_trained': detector.is_trained,
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/web/analyze', methods=['POST'])
@limiter.limit("20 per minute")
def web_analyze():
    """
    Same-origin proxy used by the web UI (templates/index.html + main.js).

    This exists so the browser never needs to hold the API key: the key
    stays server-side, and this route is reachable only from pages Flask
    itself served (no CORS headers are added for it - it's outside the
    "/api/*" CORS resource - so a browser page on another origin cannot
    call it). It performs the exact same validation/prediction as
    /api/analyze, just without the X-API-Key requirement, since the
    request never leaves the browser<->this server boundary.

    /api/analyze itself is untouched and still requires a valid API key
    for external/programmatic clients.
    """
    try:
        data = request.get_json(silent=True)
        payload, status = _perform_analysis(data)
        return jsonify(payload), status
    except Exception as e:
        logger.error(f"Error in web_analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/analyze', methods=['POST'])
@limiter.limit("20 per minute")
@require_api_key
def analyze():
    """Analyze news article with API key authentication"""
    try:
        data = request.get_json(silent=True)
        payload, status = _perform_analysis(data)
        return jsonify(payload), status
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/batch-analyze', methods=['POST'])
@limiter.limit("5 per minute")
@require_api_key
def batch_analyze():
    """Batch analysis endpoint for multiple articles"""
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({'error': 'No data provided or invalid JSON'}), 400

        if 'items' not in data:
            return jsonify({'error': 'No items provided'}), 400

        items = data['items']

        if not isinstance(items, list):
            return jsonify({'error': 'Items must be a list'}), 400

        if len(items) == 0:
            return jsonify({'error': 'Items list cannot be empty'}), 400

        if len(items) > 10:
            return jsonify({'error': 'Maximum 10 items per batch'}), 400

        results = []
        for idx, item in enumerate(items):
            try:
                if not isinstance(item, dict):
                    results.append({'item_id': idx, 'error': 'Invalid item format'})
                    continue

                input_type = item.get('type', 'text')
                content = item.get('content', '')

                # Same type validation as /api/analyze
                if input_type not in ['text', 'url']:
                    results.append({
                        'item_id': idx,
                        'error': 'Invalid input type. Use "text" or "url"'
                    })
                    continue

                if not content:
                    results.append({'item_id': idx, 'error': 'Content cannot be empty'})
                    continue

                # Get text from URL or use direct text
                if input_type == 'url':
                    text = detector.scrape_article(content)
                    if text.startswith('Error') or text.startswith('Could not'):
                        results.append({'item_id': idx, 'error': text})
                        continue
                else:
                    text = content

                # Same length validation as /api/analyze
                if len(text.strip()) < 10:
                    results.append({
                        'item_id': idx,
                        'error': 'Text too short (minimum 10 characters)'
                    })
                    continue

                if len(text) > 50000:
                    results.append({
                        'item_id': idx,
                        'error': 'Text too long (maximum 50,000 characters)'
                    })
                    continue

                prediction = detector.predict(text)
                prediction['item_id'] = idx
                results.append(prediction)

            except Exception as e:
                logger.error(f"Error processing batch item {idx}: {str(e)}", exc_info=True)
                results.append({'item_id': idx, 'error': 'Internal error processing this item'})

        return jsonify({
            'results': results,
            'total': len(results),
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in batch-analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/train', methods=['POST'])
@require_api_key
def train():
    """Train the model (admin only)"""
    # Prevent two trainings from racing on the same model/vectorizer files
    if not detector.acquire_training():
        return jsonify({
            'success': False,
            'error': 'Training already in progress. Please try again later.'
        }), 409

    try:
        logger.info("Starting model training...")
        accuracy = detector.train_model()

        logger.info(f"Model training completed. Accuracy: {accuracy:.4f}")

        return jsonify({
            'success': True,
            'accuracy': round(accuracy * 100, 2),
            'message': 'Model trained successfully!',
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Error training model: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Model training failed'
        }), 500
    finally:
        detector.release_training()


@app.route('/api/model-info', methods=['GET'])
@require_api_key
def model_info():
    """Get model information"""
    return jsonify({
        'is_trained': detector.is_trained,
        'model_type': 'Random Forest',
        'max_features': app.config['MAX_FEATURES'],
        'ngram_range': app.config['NGRAM_RANGE'],
        'accuracy': 'Not evaluated',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded from {get_remote_address()}")
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(e)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("Advanced Fake News Detection System")
    print("=" * 70)

    # Try to load existing model
    if not detector.load_model():
        logger.info("No trained model found. Training new model...")
        try:
            detector.train_model()
            logger.info("Model training completed successfully!")
        except Exception as e:
            logger.error(f"Error during initial training: {str(e)}")
            logger.info("You can train the model later using the /api/train endpoint")
    else:
        logger.info("Model loaded successfully!")

    print("\nStarting Flask server...")
    print(f"Visit: http://localhost:{app.config['PORT']}")
    print("API Documentation: Check docs/API.md")
    print("=" * 70)

    app.run(
        debug=app.config['DEBUG'],
        port=app.config['PORT'],
        host='0.0.0.0'
    )
