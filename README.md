# 📰 Advanced Fake News Analyzer

An intelligent web-based fake news detection system that analyzes news articles and predicts whether they are **REAL** or **FAKE** using Natural Language Processing and Machine Learning.

The system uses **TF-IDF feature extraction** with a **Random Forest classifier**, along with a Flask-based web interface and security-hardened API endpoints.

---

## 🚀 Features

- 🔍 **Fake News Detection**
  - Classifies news content as REAL or FAKE
  - Provides classification confidence

- 🧠 **Machine Learning**
  - TF-IDF text feature extraction
  - Random Forest classification
  - Stratified train/test evaluation
  - Duplicate-text removal during training

- 🌐 **Web Interface**
  - Clean and responsive interface
  - Text-based news analysis
  - URL-based article analysis

- 🔐 **Security**
  - API key authentication
  - Rate limiting
  - Configurable CORS
  - SSRF protection for URL analysis
  - Redirect validation
  - Response-size limits
  - Input validation
  - Generic server error responses
  - Protected model-training endpoint

- 📊 **Model Information**
  - Model status
  - Feature configuration
  - N-gram configuration
  - Model performance information

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Machine Learning | Scikit-learn |
| NLP | NLTK |
| Data Processing | Pandas, NumPy |
| Feature Extraction | TF-IDF |
| Classifier | Random Forest |
| Frontend | HTML, CSS, JavaScript |
| Dataset | ISOT Fake News Dataset |

---

## 🧠 Machine Learning Pipeline

```text
News Article
     │
     ▼
Text Preprocessing
     │
     ├── Lowercase conversion
     ├── URL removal
     ├── HTML removal
     ├── Email removal
     ├── Punctuation removal
     ├── Number removal
     └── Stop-word filtering
     │
     ▼
TF-IDF Feature Extraction
     │
     ├── Maximum Features: 1500
     └── N-grams: 1–2
     │
     ▼
Random Forest Classifier
     │
     ▼
REAL / FAKE Prediction
     │
     ▼
Confidence + Probabilities
```

---

## 📈 Model Performance

The model was trained using the **ISOT Fake News Dataset**.

After removing duplicate text samples, the training data contained:

- **17,455 Fake articles**
- **21,191 Real articles**
- **38,646 total unique samples**

The dataset was evaluated using an **80/20 stratified train-test split**.

### Test Results

| Metric | Result |
|---|---:|
| Accuracy | **99.68%** |
| Fake Precision | **1.00** |
| Fake Recall | **0.99** |
| Fake F1-Score | **1.00** |
| Real Precision | **0.99** |
| Real Recall | **1.00** |
| Real F1-Score | **1.00** |

### Confusion Matrix

```text
                 Predicted
               Fake    Real

Actual Fake    3458      22
Actual Real       3    4235
```

> **Note:** The 99.68% accuracy is the result obtained on the held-out test split of the deduplicated ISOT dataset. It should not be interpreted as universal accuracy on every type of news article or as proof that a claim is factually true or false.

---

## 🔐 Security Architecture

The application includes several security controls designed to make the API safer for real-world deployment.

### API Authentication

Protected API endpoints require an API key using the:

```text
X-API-Key
```

header.

API key comparison uses a constant-time comparison mechanism.

### Rate Limiting

API endpoints have configurable request limits to reduce abuse and excessive requests.

### SSRF Protection

URL-based article analysis includes protections against Server-Side Request Forgery (SSRF), including:

- Only HTTP/HTTPS URLs are accepted
- Private IP addresses are blocked
- Loopback addresses are blocked
- Link-local addresses are blocked
- Reserved and multicast addresses are blocked
- Cloud metadata addresses are blocked
- Redirect destinations are revalidated
- Maximum redirect count is enforced
- Maximum response size is enforced
- Network request timeout is enforced

### Same-Origin Web Analysis

The browser uses:

```text
/web/analyze
```

for web-based analysis instead of exposing the API key to client-side JavaScript.

---

## 📂 Project Structure

```text
Advanced-Fake-News-Analyzer/
│
├── app.py
├── config.py
├── detector.py
├── requirement.txt
├── README.md
│
├── data/
│   ├── Fake.csv
│   └── True.csv
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   └── index.html
│
└── docs/
    └── api.md
```

> Dataset CSV files and trained model files are excluded from the Git repository because of their size. They are required locally to train/run the full model.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/baiswarm/Advanced-Fake-News-Analyzer.git
cd Advanced-Fake-News-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Install NLTK resources

Run Python:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

For production deployment, use strong randomly generated secrets and disable Flask debug mode.

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

Open the address in your browser and enter a news article to analyze it.

---

## 🔌 API

The application provides REST API endpoints for programmatic access.

### Analyze Text

```text
POST /api/analyze
```

Required header:

```text
X-API-Key: your-api-key
```

Example request:

```json
{
  "text": "Your news article text here..."
}
```

### Batch Analysis

```text
POST /api/batch-analyze
```

Allows multiple news articles to be analyzed in a single request.

### Model Information

```text
GET /api/model-info
```

Returns information about the currently loaded model and configuration.

### Health Check

```text
GET /health
```

### Web Analysis

```text
POST /web/analyze
```

Used by the web interface for same-origin analysis.

More API details are available in:

```text
docs/api.md
```

---

## ⚠️ Important Note About Confidence

The displayed confidence is the machine-learning classifier's estimated classification probability.

For example:

```text
FAKE — 87.4%
```

does **not** mean that the system has mathematically proven the article is 87.4% factually false.

The system is a supervised text-classification model trained on labeled examples. Its predictions can be affected by the language, writing style, topic, and patterns present in the training dataset.

---

## 🎯 Use Cases

The project can be used for:

- Educational demonstrations of NLP
- Machine-learning experimentation
- News classification research
- Cybersecurity/AI portfolio projects
- Understanding text classification pipelines
- Demonstrating secure Flask API development

---

## 🔮 Future Improvements

Possible future enhancements include:

- Transformer-based models such as BERT
- External fact-checking integration
- News-source credibility analysis
- Explainable AI features
- More diverse training datasets
- Model comparison and benchmarking
- Cloud deployment
- User authentication
- Database-backed prediction history

---

## 📚 Dataset

This project uses the **ISOT Fake News Dataset**, containing labeled fake and real news articles.

The dataset is used for educational and research purposes.

---

## 👨‍💻 Author

**Manas Baiswar**

B.Tech Cybersecurity

GitHub: https://github.com/baiswarm

---

## 📄 License

This project is licensed under the MIT License.

See `LICENSE` for details.
