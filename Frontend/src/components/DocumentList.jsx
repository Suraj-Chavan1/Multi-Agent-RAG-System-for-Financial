// Document list component
import React from 'react'

const DocumentList = ({ 
  documents, 
  selectedDocuments, 
  isLoadingDocuments,
  onDocumentToggle,
  onRefresh 
}) => {
  return (
    <div className="flex-1">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-700">
          Available Documents ({documents.length})
        </h3>
        <div className="flex items-center space-x-2">
          {isLoadingDocuments && (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          )}
          <button
            onClick={onRefresh}
            disabled={isLoadingDocuments}
            className="text-xs px-2 py-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors disabled:opacity-50"
            title="Refresh document list"
          >
            🔄
          </button>
        </div>
      </div>
      
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {isLoadingDocuments ? (
          <div className="flex items-center justify-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-sm text-gray-500">Loading documents...</span>
          </div>
        ) : (
          <>
            {documents.map((doc) => (
              <div
                key={doc.document_id}
                className={`p-2 border rounded-md cursor-pointer transition-colors ${
                  selectedDocuments.includes(doc.document_id)
                    ? 'bg-blue-50 border-blue-300'
                    : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                }`}
                onClick={() => onDocumentToggle(doc.document_id)}
              >
                <div className="text-xs font-medium text-gray-900">
                  {doc.document_id}
                </div>
                <div className="text-xs text-gray-500">
                  {doc.chunk_count} chunks
                </div>
              </div>
            ))}
            {documents.length === 0 && (
              <p className="text-sm text-gray-500 italic">No documents uploaded yet</p>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default DocumentList
