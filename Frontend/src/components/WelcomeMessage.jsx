// Welcome message component
import React from 'react'

const WelcomeMessage = () => {
  return (
    <div className="text-center text-gray-500 mt-8">
      <h3 className="text-lg font-medium mb-2">Welcome to Financial RAG System!</h3>
      <p className="mb-4">Ask questions about stocks or upload documents for analysis.</p>
      <div className="text-sm space-y-1">
        <p>• <strong>Without documents:</strong> Get live stock data</p>
        <p>• <strong>With documents:</strong> Search uploaded PDFs</p>
      </div>
    </div>
  )
}

export default WelcomeMessage
