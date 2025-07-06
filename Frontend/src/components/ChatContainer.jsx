// Main chat container component
import React from 'react'
import ChatArea from './ChatArea'
import ChatInput from './ChatInput'

const ChatContainer = ({ 
  messages, 
  currentMessage, 
  setCurrentMessage, 
  onSendMessage, 
  isLoading,
  selectedDocuments 
}) => {
  return (
    <div className="flex-1 flex flex-col">
      <ChatArea messages={messages} isLoading={isLoading} />
      
      <ChatInput
        currentMessage={currentMessage}
        setCurrentMessage={setCurrentMessage}
        onSendMessage={onSendMessage}
        isLoading={isLoading}
        selectedDocuments={selectedDocuments}
      />
    </div>
  )
}

export default ChatContainer
