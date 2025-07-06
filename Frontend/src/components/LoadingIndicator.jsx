// Loading indicator component
import React from 'react'

const LoadingIndicator = () => {
  return (
    <div className="flex justify-start">
      <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span className="text-sm text-gray-600">Thinking...</span>
        </div>
      </div>
    </div>
  )
}

export default LoadingIndicator
