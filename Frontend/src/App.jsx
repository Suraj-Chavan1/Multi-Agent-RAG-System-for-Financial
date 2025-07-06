import React from 'react'
import './App.css'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatContainer from './components/ChatContainer'
import { useFinancialRAG } from './hooks/useFinancialRAG'

function App() {
  const {
    // State
    messages,
    currentMessage,
    setCurrentMessage,
    symbol,
    setSymbol,
    documents,
    selectedDocuments,
    isLoading,
    isUploading,
    isLoadingDocuments,
    showUpload,
    setShowUpload,
    
    // Actions
    sendMessage,
    uploadDocument,
    toggleDocumentSelection,
    loadDocuments
  } = useFinancialRAG()

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />

      {/* Main Content */}
      <div className="flex-1 flex max-w-6xl mx-auto w-full">
        <Sidebar
          symbol={symbol}
          setSymbol={setSymbol}
          documents={documents}
          selectedDocuments={selectedDocuments}
          isUploading={isUploading}
          isLoadingDocuments={isLoadingDocuments}
          showUpload={showUpload}
          setShowUpload={setShowUpload}
          onDocumentUpload={uploadDocument}
          onDocumentToggle={toggleDocumentSelection}
          onDocumentRefresh={loadDocuments}
        />

        <ChatContainer
          messages={messages}
          currentMessage={currentMessage}
          setCurrentMessage={setCurrentMessage}
          onSendMessage={sendMessage}
          isLoading={isLoading}
          selectedDocuments={selectedDocuments}
        />
      </div>
    </div>
  )
}

export default App
