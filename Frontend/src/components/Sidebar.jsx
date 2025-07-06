// Sidebar component that combines all sidebar elements
import React from 'react'
import SymbolInput from './SymbolInput'
import DocumentUpload from './DocumentUpload'
import DocumentList from './DocumentList'
import SelectedDocumentsInfo from './SelectedDocumentsInfo'

const Sidebar = ({
  symbol,
  setSymbol,
  documents,
  selectedDocuments,
  isUploading,
  isLoadingDocuments,
  showUpload,
  setShowUpload,
  onDocumentUpload,
  onDocumentToggle,
  onDocumentRefresh
}) => {
  return (
    <div className="w-80 bg-white border-r border-gray-200 p-4 flex flex-col">
      <SymbolInput symbol={symbol} setSymbol={setSymbol} />
      
      <DocumentUpload
        isUploading={isUploading}
        showUpload={showUpload}
        setShowUpload={setShowUpload}
        onUpload={onDocumentUpload}
      />

      <DocumentList
        documents={documents}
        selectedDocuments={selectedDocuments}
        isLoadingDocuments={isLoadingDocuments}
        onDocumentToggle={onDocumentToggle}
        onRefresh={onDocumentRefresh}
      />

      <SelectedDocumentsInfo selectedDocuments={selectedDocuments} />
    </div>
  )
}

export default Sidebar
