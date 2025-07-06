// Selected documents info component
import React from 'react'

const SelectedDocumentsInfo = ({ selectedDocuments }) => {
  if (selectedDocuments.length === 0) return null

  return (
    <div className="mt-4 p-2 bg-blue-50 rounded-md">
      <p className="text-xs text-blue-700">
        📄 {selectedDocuments.length} document(s) selected
      </p>
      <p className="text-xs text-blue-600">
        Questions will search these documents
      </p>
    </div>
  )
}

export default SelectedDocumentsInfo
