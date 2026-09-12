# 🔍 Advanced Fake News Detection System

An intelligent web application that leverages Machine Learning and Natural Language Processing to detect fake news articles with high accuracy. Built with Flask, scikit-learn, and NLTK.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-92.3%25-brightgreen.svg)

## ✨ Features

- **High Accuracy**: Achieves 92.3% accuracy using Random Forest classification
- **Real-time Analysis**: Sub-100ms prediction times
- **Dual Input Modes**: Analyze text directly or extract from URLs
- **Confidence Scoring**: Transparent probability distribution for predictions
- **Modern Web Interface**: Responsive design with gradient animations
- **API Integration**: RESTful API for external integrations
- **Model Persistence**: Save and load trained models
- **Extensible Architecture**: Easy to integrate additional ML models

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/manasbaiswar/fake-news-detection.git
cd fake-news-detection
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your configuration
```

5. **Download NLTK data**
```bash
python setup_nltk.py
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
```
Open your browser and navigate to: http://localhost:5000
```

## 📁 Project Structure

```
fake-news-detection/
│
├── app.py                      # Main Flask application
├── detector.py                 # Fake news detector class
├── config.py                   # Configuration settings
├── setup_nltk.py              # NLTK setup script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── templates/
│   └── index.html             # Web interface
│
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet
│   └── js/
│       └── main.js            # JavaScript logic
│
├── models/                     # Saved ML models (generated)
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── data/                       # Training datasets
│   ├── Fake.csv
│   └── True.csv
│
└── docs/
    ├── API.md                  # API documentation
    └── DEPLOYMENT.md           # Deployment guide
```

## 🔧 Configuration

Edit the `.env` file to configure:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Model Configuration
MODEL_PATH=models/model.pkl
VECTORIZER_PATH=models/vectorizer.pkl
MAX_FEATURES=5000
NGRAM_RANGE=1,3

# API Configuration
API_RATE_LIMIT=100
API_KEY=your-api-key-here

# News API (optional)
NEWS_API_KEY=your-news-api-key
```

## 📊 API Endpoints

### Analyze Text

```bash
POST /api/analyze
Content-Type: application/json
X-API-Key: your-api-key

{
  "type": "text",
  "content": "Your news article text here"
}
```

### Analyze URL

```bash
POST /api/analyze
Content-Type: application/json
X-API-Key: your-api-key

{
  "type": "url",
  "content": "https://example.com/article"
}
```

### Train Model

```bash
POST /api/train
X-API-Key: your-api-key
```

See [API.md](docs/API.md) for complete API documentation.

## 🧪 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 92.3% |
| Precision | 91.8% |
| Recall | 92.7% |
| F1-Score | 92.2% |

## 🛠️ Technology Stack

- **Backend**: Flask, Python 3.8+
- **Machine Learning**: scikit-learn, Random Forest
- **NLP**: NLTK, TF-IDF Vectorization
- **Web Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Data Processing**: pandas, numpy

## 📈 How It Works

1. **Text Preprocessing**: Removes URLs, HTML tags, special characters, and stopwords
2. **Feature Extraction**: Converts text to TF-IDF vectors (5000 features, 1-3 grams)
3. **Classification**: Random Forest classifier (100 trees, max depth 20)
4. **Prediction**: Returns label with confidence score and probability distribution

## 🔒 Security Features

- API key authentication
- Rate limiting
- Input validation and sanitization
- CORS configuration
- Environment variable protection

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Manas Baiswar**

- GitHub: [@manasbaiswar](https://github.com/manasbaiswar)
- Email: baiswarm@gmail.com
  

## 🙏 Acknowledgments

- DIT University, Dehradun
- Kaggle for the Fake and Real News Dataset
- NLTK and scikit-learn communities

## 🔮 Future Enhancements

- [ ] Deep Learning integration (BERT/RoBERTa)
- [ ] Multilingual support
- [ ] Fact-checking API integration
- [ ] Browser extension
- [ ] Mobile application
- [ ] Image and video analysis
- [ ] Real-time monitoring dashboard

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the author.

---

⭐ If you find this project useful, please consider giving it a star!
