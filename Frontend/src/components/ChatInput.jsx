// Chat input component
import React from 'react'

const ChatInput = ({ 
  currentMessage, 
  setCurrentMessage, 
  onSendMessage, 
  isLoading,
  selectedDocuments 
}) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSendMessage()
    }
  }

  return (
    <div className="border-t border-gray-200 p-4">
      <div className="flex space-x-2">
        <textarea
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about stocks or document content..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="1"
          style={{ minHeight: '40px', maxHeight: '120px' }}
        />
        <button
          onClick={onSendMessage}
          disabled={!currentMessage.trim() || isLoading}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Send
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-2">
        {selectedDocuments.length > 0 
          ? `🔍 Searching ${selectedDocuments.length} document(s)`
          : '📈 Getting live financial data'
        }
      </p>
    </div>
  )
}

export default ChatInput
