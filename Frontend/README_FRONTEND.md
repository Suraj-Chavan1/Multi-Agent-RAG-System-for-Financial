# Financial RAG System - Frontend

A simple React chat interface for the Financial RAG System.

## Features

- 💬 **Chat Interface**: Ask questions about stocks or documents
- 📄 **Document Upload**: Upload PDF documents for analysis
- 🔍 **Document Selection**: Choose specific documents to search
- 📈 **Live Data**: Get real-time financial data when no documents selected
- 🎯 **Smart Routing**: Automatically routes between live data and document search

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Make sure the backend is running on http://localhost:8000**

## Usage

### Getting Live Stock Data
- Select a stock symbol (e.g., AAPL, MSFT)
- Ask questions without selecting any documents
- Example: "What is the current stock price?"

### Searching Documents
- Upload PDF documents using the "Upload Document" button
- Select documents from the sidebar
- Ask questions about the document content
- Example: "What were the earnings highlights?"

## How It Works

The frontend automatically determines how to route your query:

- **No documents selected** → Gets live financial data via yfinance
- **Documents selected** → Searches uploaded PDFs using RAG

## API Endpoints

The frontend connects to these backend endpoints:
- `POST /query` - Send questions
- `POST /upload` - Upload PDF documents
- `GET /documents` - List uploaded documents
- `GET /health` - Health check

## Technology Stack

- **React 19** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Fetch API** - HTTP requests
