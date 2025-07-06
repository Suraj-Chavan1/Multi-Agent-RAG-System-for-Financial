// Document upload component
import React, { useRef } from 'react'

const DocumentUpload = ({ 
  isUploading, 
  showUpload, 
  setShowUpload, 
  onUpload 
}) => {
  const fileInputRef = useRef(null)

  const handleFileChange = (event) => {
    onUpload(event)
  }

  return (
    <div className="mb-4">
      <button
        onClick={() => setShowUpload(!showUpload)}
        disabled={isUploading}
        className={`w-full px-4 py-2 rounded-md transition-colors ${
          isUploading 
            ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
            : 'bg-green-600 text-white hover:bg-green-700'
        }`}
      >
        {isUploading ? (
          <div className="flex items-center justify-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            <span>Uploading...</span>
          </div>
        ) : (
          '📄 Upload Document'
        )}
      </button>
      
      {showUpload && !isUploading && (
        <div className="mt-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={isUploading}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
          />
          <p className="text-xs text-gray-500 mt-1">Only PDF files supported</p>
        </div>
      )}
      
      {isUploading && (
        <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-sm text-blue-700">Processing document...</span>
          </div>
          <div className="mt-1">
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{width: '70%'}}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DocumentUpload
