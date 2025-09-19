# 🔍 DetectAI: Misinformation Detection System

A comprehensive AI-powered misinformation detection system that analyzes text content to determine its credibility and potential for being misinformation using Google Gemini AI.

## ✨ Features

- 🤖 **Google Gemini AI Integration** - Advanced text analysis using Google's Gemini 2.0 Flash model
- 🎨 **Streamlit Web Interface** - Beautiful, interactive web UI for easy content analysis
- 🔍 **Intelligent Claim Analysis** - AI-powered extraction and fact-checking of key claims
- 📊 **Credibility Scoring** - Numerical scoring system for content reliability
- 🔄 **Real-time Analysis** - Live status updates and progress tracking
- 🛡️ **Robust Error Handling** - Graceful fallbacks and comprehensive error management
- 🧪 **Comprehensive Testing** - Full test suite for reliability and quality assurance
- 🐳 **Docker Ready** - Containerized deployment for easy scaling

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - Main programming language
- **Node.js 18+** - For React frontend (optional)
- **Google Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Git** - For cloning the repository

### 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd misinformation-detector
   ```

2. **Install Python dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic google-generativeai python-dotenv streamlit requests alembic asyncpg python-multipart httpx
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   **Edit the `.env` file and add your Gemini API key:**
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   GEMINI_MODEL=gemini-2.0-flash
   DATABASE_URL=sqlite:///./misinformation_detector.db
   ```

   **🔑 Get your Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key to your `.env` file

4. **Initialize the database:**
   ```bash
   python manage_db.py
   ```

### 🎯 Running the Application

You have two frontend options to choose from:

### 🎨 Run Streamlit Application

1. **Start the Streamlit app:**
   ```bash
   python -m streamlit run streamlitui.py --server.port 8501
   ```

2. **Access the application:**
   - **Streamlit UI**: http://localhost:8501

**Note:** The app runs as a standalone Streamlit application with built-in AI analysis.

## 📖 How to Use

### Using the Streamlit Web Interface

1. **Navigate to** http://localhost:8501
2. **Enter or upload text** content you want to analyze
3. **Configure settings** in the sidebar (optional):
   - Backend API URL
   - Max claims to analyze
   - Analysis timeout
4. **Click "Analyze for Misinformation"**
5. **View results** with credibility score, claims analysis, and recommendations

### Using the API Directly

#### Analyze Text Content
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Climate change is caused by solar radiation variations."}'
```

#### Check System Health
```bash
curl -X GET "http://localhost:8000/health"
```

#### Example Analysis Response
```json
{
  "overall_assessment": "LIKELY_INACCURATE",
  "credibility_score": 0.25,
  "summary": "The claim about solar radiation being the primary cause of climate change contradicts scientific consensus...",
  "claims": [
    {
      "text": "Climate change is caused by solar radiation variations",
      "credibility": "low",
      "evidence": "Scientific consensus attributes climate change primarily to greenhouse gas emissions..."
    }
  ],
  "recommendations": [
    "Verify claims against peer-reviewed scientific sources",
    "Check IPCC reports for climate science consensus"
  ]
}
```

## 🔧 API Reference

### Main Endpoints

#### `POST /analyze`
**Direct analysis endpoint for immediate results**

**Request:**
```json
{
  "text": "Text content to analyze",
  "max_claims": 5,
  "timeout": 30
}
```

**Response:**
```json
{
  "overall_assessment": "CREDIBLE|SUSPICIOUS|MISINFORMATION",
  "credibility_score": 0.85,
  "summary": "Analysis summary...",
  "claims": [
    {
      "text": "Extracted claim",
      "credibility": "high|medium|low",
      "evidence": "Supporting evidence or concerns"
    }
  ],
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}
```

#### `POST /analysis`
**Asynchronous analysis with status tracking**

**Request:**
```json
{
  "content": "Text content to analyze"
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "PENDING|PROCESSING|COMPLETE|FAILED",
  "content_to_analyze": "Text content",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `GET /analysis/{analysis_id}`
**Retrieve analysis results by ID**

#### `GET /health`
**System health check**

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "available",
  "version": "0.1.0"
}
```

### Assessment Categories
- **CREDIBLE**: Content appears reliable and well-supported
- **SUSPICIOUS**: Content has some questionable elements
- **MISINFORMATION**: Content likely contains false information

## 📁 Project Structure

```
misinformation-detector/
├── app/                    # 🚀 Backend FastAPI application
│   ├── __init__.py
│   ├── main.py            # FastAPI app, endpoints, and middleware
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── agent.py           # 🤖 Google Gemini AI integration
│   ├── database.py        # Database configuration and connection
│   └── database_init.py   # Database initialization utilities

├── tests/                 # 🧪 Test suite
│   ├── test_models.py     # Database model tests
│   ├── test_api.py        # API endpoint tests
│   └── test_agent.py      # AI agent tests
├── alembic/               # 🗄️ Database migrations
├── .kiro/                 # 📋 Kiro specification files
│   └── specs/
│       └── misinformation-detector/
├── streamlitui.py         # 🎨 Streamlit web interface (main UI)
├── manage_db.py           # 🔧 Database management utility
├── pyproject.toml         # Python dependencies and configuration
├── Dockerfile             # 🐳 Docker container configuration
├── .env.example           # Environment variables template
├── .env                   # Your environment variables (create this)
└── README.md              # This documentation
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
pytest tests/test_api.py      # API endpoint tests
pytest tests/test_models.py   # Database model tests
pytest tests/test_agent.py    # AI agent tests
```

### Quick Integration Test
```bash
python test_agent_quick.py   # Quick AI agent functionality test
python test_gemini_agent.py  # Gemini API integration test
```

## Docker Deployment

### Build and Run Locally
```bash
# Build the Docker image
docker build -t misinformation-detector .

# Run the container
docker run -p 8080:8080 misinformation-detector
```

### Cloud Run Deployment
The application is configured for Google Cloud Run deployment:

```bash
# Build for Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/misinformation-detector

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT_ID/misinformation-detector --platform managed
```

## 🛠️ Development

### Environment Setup
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install pytest black isort flake8 mypy
```

### Code Quality
```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Type checking
mypy app/
```

### Adding New Features
1. Check `.kiro/specs/misinformation-detector/` for requirements and design
2. Implement the feature in the appropriate module
3. Add comprehensive tests
4. Update documentation
5. Test with both UIs (Streamlit and React)

## 🏗️ Architecture

### System Components
1. **🎨 Frontend Layer**: Streamlit UI (primary) + React UI (alternative)
2. **🚀 API Layer**: FastAPI with automatic documentation
3. **🤖 AI Layer**: Google Gemini integration for content analysis
4. **🗄️ Data Layer**: SQLite database with SQLAlchemy ORM

### Analysis Workflow
1. **Input**: User submits text via Streamlit UI or API
2. **Processing**: Google Gemini AI analyzes content for:
   - Key claim extraction
   - Fact verification
   - Credibility assessment
   - Evidence evaluation
3. **Output**: System returns:
   - Overall credibility score (0.0 - 1.0)
   - Detailed claim analysis
   - Supporting evidence or concerns
   - Actionable recommendations

### Key Technologies
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **AI**: Google Gemini 2.0 Flash
- **Frontend**: Streamlit (primary), React (alternative)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Deployment**: Docker, Google Cloud Run ready

## 🚨 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if `.env` file exists and contains `GEMINI_API_KEY`
- Verify Python dependencies are installed
- Ensure port 8000 is not in use

**Streamlit UI shows "Backend Offline":**
- Make sure FastAPI backend is running on port 8000
- Check the API URL in Streamlit sidebar settings
- Verify firewall/antivirus isn't blocking connections

**Analysis returns errors:**
- Verify your Gemini API key is valid and has quota
- Check internet connection for API calls
- Review backend logs for detailed error messages

**React frontend issues:**
- Run `npm install` in the frontend directory
- Check if port 3000 is available
- Verify Node.js version is 18+

### Getting Help
1. Check the API documentation at http://localhost:8000/docs
2. Review test files for usage examples
3. Check system health at http://localhost:8000/health

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

**Built with ❤️ using Google Gemini AI, FastAPI, and Streamlit**