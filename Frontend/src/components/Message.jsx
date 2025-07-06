// Individual message component
import React from 'react'

const Message = ({ message }) => {
  return (
    <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        message.type === 'user' 
          ? 'bg-blue-600 text-white'
          : message.type === 'error'
          ? 'bg-red-100 text-red-800 border border-red-200'
          : message.type === 'system'
          ? 'bg-green-100 text-green-800 border border-green-200'
          : 'bg-white text-gray-800 border border-gray-200'
      }`}>
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <div className="flex justify-between items-center mt-1">
          <p className="text-xs opacity-70">{message.timestamp}</p>
          {message.route && (
            <span className={`text-xs px-2 py-1 rounded ${
              message.route === 'financial_agent_yfinance' 
                ? 'bg-blue-100 text-blue-700'
                : 'bg-purple-100 text-purple-700'
            }`}>
              {message.route === 'financial_agent_yfinance' ? '📈 Live Data' : '📄 Documents'}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default Message
