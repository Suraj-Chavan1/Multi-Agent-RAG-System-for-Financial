// Custom hook for managing chat and document state
import { useState, useEffect } from 'react'

const API_BASE_URL = 'https://multi-agent-rag-system-for-financial-2.onrender.com'

export const useFinancialRAG = () => {
  // State management
  const [messages, setMessages] = useState([])
  const [currentMessage, setCurrentMessage] = useState('')
  const [symbol, setSymbol] = useState('AAPL')
  const [documents, setDocuments] = useState([])
  const [selectedDocuments, setSelectedDocuments] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(false)
  const [showUpload, setShowUpload] = useState(false)

  // Load documents on mount
  useEffect(() => {
    loadDocuments()
  }, [])

  // Document management
  const loadDocuments = async () => {
    try {
      setIsLoadingDocuments(true)
      const response = await fetch(`${API_BASE_URL}/documents`)
      const data = await response.json()
      if (data.success) {
        setDocuments(data.documents || [])
      }
    } catch (error) {
      console.error('Error loading documents:', error)
    } finally {
      setIsLoadingDocuments(false)
    }
  }

  // Message sending
  const sendMessage = async () => {
    if (!currentMessage.trim()) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: currentMessage,
      timestamp: new Date().toLocaleTimeString()
    }

    setMessages(prev => [...prev, userMessage])
    setCurrentMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentMessage,
          symbol: symbol,
          document_ids: selectedDocuments.length > 0 ? selectedDocuments : null
        }),
      })

      const data = await response.json()
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.answer,
        route: data.route_taken,
        timestamp: new Date().toLocaleTimeString()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: 'Sorry, something went wrong. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // Document upload
  const uploadDocument = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      setIsUploading(true)
      
      // Show upload start message
      const uploadStartMessage = {
        id: Date.now(),
        type: 'system',
        content: `📤 Uploading "${file.name}"...`,
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, uploadStartMessage])

      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      
      if (data.success) {
        const successMessage = {
          id: Date.now() + 1,
          type: 'system',
          content: `✅ Document uploaded successfully! Document ID: ${data.document_id}`,
          timestamp: new Date().toLocaleTimeString()
        }
        setMessages(prev => [...prev, successMessage])
        
        // Refresh documents list
        await loadDocuments()
        setShowUpload(false)
        
        // Show refresh notification
        const refreshMessage = {
          id: Date.now() + 2,
          type: 'system',
          content: `🔄 Document list refreshed - ${file.name} is now available for selection`,
          timestamp: new Date().toLocaleTimeString()
        }
        setMessages(prev => [...prev, refreshMessage])
        
      } else {
        throw new Error(data.message || 'Upload failed')
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        type: 'error', 
        content: `❌ Upload failed: ${error.message}`,
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsUploading(false)
    }
  }

  // Document selection toggle
  const toggleDocumentSelection = (docId) => {
    setSelectedDocuments(prev => 
      prev.includes(docId) 
        ? prev.filter(id => id !== docId)
        : [...prev, docId]
    )
  }

  return {
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
  }
}
