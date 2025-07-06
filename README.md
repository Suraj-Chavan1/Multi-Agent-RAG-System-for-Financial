# 💼 Multi-Agent RAG System for Financial Analysis

A production-ready Financial RAG (Retrieval-Augmented Generation) system that intelligently routes queries between live financial data (yfinance) and document-based analysis (PDF RAG) using FastAPI backend and React frontend.

## 🎯 Key Features

- **Intelligent Routing**: Automatically routes queries based on document selection
- **Document Upload**: PDF document processing with text extraction and chunking
- **Vector Storage**: Pinecone vector database for semantic search
- **Real-time Financial Data**: Integration with yfinance for live market data
- **Modern UI**: React frontend with Tailwind CSS styling
- **Symbol Independence**: RAG system operates purely on document content, not stock symbols

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   Vector Store   │
│                 │◄──►│                 │◄──►│   (Pinecone)    │
│  - Document UI  │    │  - Orchestrator │    │                 │
│  - Chat Interface│    │  - Agents       │    │  - Embeddings   │
│  - File Upload  │    │  - Routing      │    │  - Similarity   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  External APIs  │
                       │                 │
                       │  - yfinance     │
                       │  - Gemini AI    │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- Pinecone API key
- Google Gemini API key

### Backend Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Suraj-Chavan1/Multi-Agent-RAG-System-for-Financial.git
   cd Multi-Agent-RAG-System-for-Financial/app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create `.env` file in the `app` directory:
   ```env
   # Pinecone Configuration
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=financial-rag-768
   PINECONE_ENVIRONMENT=us-east-1

   # Gemini AI Configuration
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL_NAME=gemini-2.5-flash
   GEMINI_EMBEDDING_MODEL=models/embedding-001
   ```

5. **Start the backend server:**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../Frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📖 Usage

### Document Upload and Analysis

1. **Upload PDFs**: Click "Upload Document" and select PDF files
2. **Select Documents**: Choose documents from the sidebar for analysis
3. **Ask Questions**: Type questions about the selected documents

### Financial Data Queries

1. **Enter Stock Symbol**: Type symbol (e.g., AAPL, MSFT) in the sidebar
2. **Ask Questions**: Ask about stock prices, financial metrics without selecting documents
3. **Get Live Data**: Receive real-time financial information

### Routing Logic

- **With Documents Selected** → RAG Agent (PDF Analysis)
- **No Documents Selected** → Financial Agent (Live Data)

## 🔧 API Endpoints

### Core Endpoints

- `POST /query` - Main query endpoint with intelligent routing
- `POST /upload` - Upload PDF documents
- `GET /documents` - List uploaded documents
- `GET /health` - Health check

### Example API Usage

```python
import requests

# Upload document
with open('financial_report.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )

# Query with document
response = requests.post(
    'http://localhost:8000/query',
    json={
        'question': 'What are the revenue highlights?',
        'symbol': 'AAPL',
        'document_ids': ['your_document_id']
    }
)
```

## 🧩 Component Architecture

### Backend Components

- **`main.py`** - FastAPI application and endpoints
- **`orchestrator.py`** - Central routing logic
- **`agents/document_agent.py`** - PDF processing and RAG
- **`agents/financial_agent.py`** - yfinance integration

### Frontend Components

- **`App.jsx`** - Main application component
- **`components/Header.jsx`** - Application header
- **`components/Sidebar.jsx`** - Document and symbol management
- **`components/ChatContainer.jsx`** - Chat interface
- **`hooks/useFinancialRAG.js`** - Business logic hook

## 🧪 Testing

### Backend Tests

```bash
cd app

# Test document upload
python test_symbol_independence.py

# Test API endpoints
python test_api_symbol_independence.py

# Clear database
python clear_pinecone_now.py
```

### Frontend Testing

```bash
cd Frontend

# Run component tests
npm test

# Build for production
npm run build
```

## 🛠️ Development

### Database Management

```bash
# List all documents
python -c "import asyncio; from agents.document_agent import DocumentAgent; asyncio.run(DocumentAgent().list_documents())"

# Clear all data
python clear_pinecone_now.py

# Upload test document
python agents/test_document_agent.py
```

### Adding New Components

1. Create component in `Frontend/src/components/`
2. Export from `Frontend/src/components/index.js`
3. Import and use in parent components

## 📊 Monitoring

- **Backend Logs**: Check terminal running uvicorn
- **Frontend Logs**: Check browser developer console
- **Pinecone Usage**: Monitor via Pinecone dashboard
- **API Usage**: Monitor via Google AI Studio

## 🚨 Troubleshooting

### Common Issues

1. **Pinecone Connection Failed**
   - Verify API key in `.env`
   - Check index name and dimensions (768)

2. **Gemini API Quota Exceeded**
   - Check API limits in Google AI Studio
   - Implement retry logic for quota management

3. **Document Upload Failed**
   - Ensure PDF files are not corrupted
   - Check file size limits (< 10MB recommended)

4. **Frontend Build Issues**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pinecone** for vector database services
- **Google Gemini** for AI/ML capabilities
- **yfinance** for financial data access
- **FastAPI** for backend framework
- **React** for frontend framework

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check the [documentation](./docs/)
- Review the [FAQ](./docs/FAQ.md)

---

**Built with ❤️ for the Financial AI Community**
