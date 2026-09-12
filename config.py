"""
Configuration settings for the application
Author: Manas Baiswar
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # Insecure placeholder values shipped in .env.example. If these are still
    # in effect while DEBUG is off (i.e. a production-like run), startup
    # should fail rather than silently run with known-default secrets.
    _DEFAULT_SECRET_KEY = 'dev-secret-key-change-in-production'
    _DEFAULT_API_KEY = 'your-default-api-key-here'

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', _DEFAULT_SECRET_KEY)
    # DEBUG defaults to False. Developers who want the Werkzeug debugger
    # locally must explicitly opt in via FLASK_DEBUG=True in their .env.
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))

    # API settings
    API_KEY = os.getenv('API_KEY', _DEFAULT_API_KEY)
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))

    # Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/model.pkl')
    VECTORIZER_PATH = os.getenv('VECTORIZER_PATH', 'models/vectorizer.pkl')
    MAX_FEATURES = int(os.getenv('MAX_FEATURES', 1500))
    NGRAM_RANGE = tuple(map(int, os.getenv('NGRAM_RANGE', '1,2').split(',')))

    # Data settings
    FAKE_CSV = os.getenv('FAKE_CSV', 'data/Fake.csv')
    TRUE_CSV = os.getenv('TRUE_CSV', 'data/True.csv')

    # External API keys (optional)
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    @classmethod
    def get_cors_origins(cls):
        """Return CORS_ORIGINS as '*' or a list of allowed origins."""
        raw = (cls.CORS_ORIGINS or '*').strip()
        if raw == '*':
            return '*'
        origins = [o.strip() for o in raw.split(',') if o.strip()]
        return origins if origins else '*'

    @classmethod
    def validate(cls):
        """
        Fail fast at startup if running non-debug (production-like) with
        insecure placeholder secrets still in place. Local development with
        FLASK_DEBUG=True is left usable without forcing real secrets.
        """
        if cls.DEBUG:
            return

        problems = []
        if cls.SECRET_KEY == cls._DEFAULT_SECRET_KEY:
            problems.append(
                "SECRET_KEY is still the insecure default placeholder value."
            )
        if cls.API_KEY == cls._DEFAULT_API_KEY:
            problems.append(
                "API_KEY is still the insecure default placeholder value."
            )

        if problems:
            raise RuntimeError(
                "Refusing to start with insecure production configuration: "
                + " ".join(problems)
                + " Set real secrets via environment variables (SECRET_KEY, "
                  "API_KEY), or set FLASK_DEBUG=True for local development."
            )