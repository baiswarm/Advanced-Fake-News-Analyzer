# API Documentation

## Authentication

All API endpoints require authentication using an API key. Include your API key in the request headers:

```
X-API-Key: your-api-key-here
```

## Base URL

```
http://localhost:5000/api
```

## Rate Limiting

- Default: 100 requests per hour
- Analyze endpoint: 20 requests per minute
- Batch analyze: 5 requests per minute

## Endpoints

### 1. Analyze Text

Analyze a single news article for fake news detection.

**Endpoint:** `POST /api/analyze`

**Headers:**
```
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body (Text):**
```json
{
  "type": "text",
  "content": "Your news article text here..."
}
```

**Request Body (URL):**
```json
{
  "type": "url",
  "content": "https://example.com/article"
}
```

**Response:**
```json
{
  "prediction": "FAKE",
  "confidence": 94.73,
  "label": 0,
  "probabilities": {
    "fake": 94.73,
    "real": 5.27
  },
  "features": {
    "word_count": 156,
    "sensational_count": 3,
    "emotional_count": 2
  },
  "timestamp": "2025-01-20T10:30:00",
  "input_type": "text",
  "text_length": 892
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid input)
- `401`: Unauthorized (missing API key)
- `403`: Forbidden (invalid API key)
- `429`: Rate limit exceeded
- `500`: Internal server error

---

### 2. Batch Analyze

Analyze multiple articles in a single request.

**Endpoint:** `POST /api/batch-analyze`

**Headers:**
```
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**
```json
{
  "items": [
    {
      "type": "text",
      "content": "First article text..."
    },
    {
      "type": "url",
      "content": "https://example.com/article2"
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "item_id": 0,
      "prediction": "FAKE",
      "confidence": 92.5,
      "label": 0,
      "probabilities": {
        "fake": 92.5,
        "real": 7.5
      }
    },
    {
      "item_id": 1,
      "prediction": "REAL",
      "confidence": 88.3,
      "label": 1,
      "probabilities": {
        "fake": 11.7,
        "real": 88.3
      }
    }
  ],
  "total": 2,
  "timestamp": "2025-01-20T10:35:00"
}
```

**Limitations:**
- Maximum 10 items per batch

---

### 3. Train Model

Train or retrain the machine learning model.

**Endpoint:** `POST /api/train`

**Headers:**
```
X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "success": true,
  "accuracy": 92.3,
  "message": "Model trained successfully!",
  "timestamp": "2025-01-20T10:40:00"
}
```

---

### 4. Model Information

Get information about the current model.

**Endpoint:** `GET /api/model-info`

**Headers:**
```
X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "is_trained": true,
  "model_type": "Random Forest",
  "max_features": 5000,
  "ngram_range": [1, 3],
  "accuracy": "92.3%",
  "timestamp": "2025-01-20T10:45:00"
}
```

---

### 5. Health Check

Check if the API is running (no authentication required).

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_trained": true,
  "timestamp": "2025-01-20T10:50:00"
}
```

---

## Example Usage

### Python

```python
import requests

API_KEY = "your-api-key-here"
BASE_URL = "http://localhost:5000/api"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Analyze text
data = {
    "type": "text",
    "content": "SHOCKING: Scientists discover miracle cure!"
}

response = requests.post(
    f"{BASE_URL}/analyze",
    json=data,
    headers=headers
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}%")
```

### cURL

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "type": "text",
    "content": "Your news article here..."
  }'
```

### JavaScript

```javascript
const API_KEY = "your-api-key-here";
const BASE_URL = "http://localhost:5000/api";

async function analyzeNews(text) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({
      type: "text",
      content: text
    })
  });
  
  const result = await response.json();
  return result;
}

// Usage
analyzeNews("Your article text here")
  .then(result => console.log(result));
```

---

## Error Handling

All errors return a JSON response with an `error` field:

```json
{
  "error": "Error description here",
  "details": "Additional details (optional)"
}
```

Common errors:
- Missing API key
- Invalid API key
- Rate limit exceeded
- Empty or too short content
- URL scraping failed
- Model not trained

---

## Best Practices

1. **Always validate input** before sending to API
2. **Handle rate limits** gracefully with exponential backoff
3. **Cache results** when appropriate to reduce API calls
4. **Use batch analyze** for multiple articles to save requests
5. **Monitor API key usage** and rotate keys periodically
6. **Check health endpoint** before making requests
7. **Handle errors** properly in your application
