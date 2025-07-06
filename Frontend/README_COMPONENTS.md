# Frontend Component Architecture

The React frontend has been refactored into smaller, reusable components for better maintainability and organization.

## 📁 Project Structure

```
src/
├── App.jsx                    # Main application component
├── App.css                    # Global styles
├── components/                # Reusable UI components
│   ├── Header.jsx            # Application header
│   ├── Sidebar.jsx           # Main sidebar container
│   ├── SymbolInput.jsx       # Stock symbol input field
│   ├── DocumentUpload.jsx    # Document upload component
│   ├── DocumentList.jsx      # List of available documents
│   ├── SelectedDocumentsInfo.jsx # Selected documents info
│   ├── ChatContainer.jsx     # Main chat area container
│   ├── ChatArea.jsx          # Messages display area
│   ├── ChatInput.jsx         # Message input component
│   ├── Message.jsx           # Individual message component
│   ├── WelcomeMessage.jsx    # Welcome/intro message
│   └── LoadingIndicator.jsx  # Loading spinner component
└── hooks/
    └── useFinancialRAG.js    # Custom hook for business logic
```

## 🧩 Component Breakdown

### Core Components

#### `App.jsx`
- Main application container
- Combines all major sections
- Uses the `useFinancialRAG` hook for state management

#### `Header.jsx`
- Application title and description
- Static component

#### `Sidebar.jsx`
- Container for all sidebar functionality
- Combines SymbolInput, DocumentUpload, DocumentList, and SelectedDocumentsInfo

#### `ChatContainer.jsx`
- Main chat interface container
- Combines ChatArea and ChatInput

### UI Components

#### `SymbolInput.jsx`
- Stock symbol input field
- Handles symbol state updates

#### `DocumentUpload.jsx`
- File upload functionality
- Shows upload progress and loading states
- Handles file selection and upload process

#### `DocumentList.jsx`
- Displays available documents
- Handles document selection/deselection
- Shows loading state while fetching documents
- Includes refresh button

#### `SelectedDocumentsInfo.jsx`
- Shows count of selected documents
- Displays when documents are selected for search

#### `ChatArea.jsx`
- Message display area
- Handles scrolling to bottom
- Shows welcome message when empty
- Includes loading indicator

#### `ChatInput.jsx`
- Message input textarea
- Send button
- Shows context info (document search vs live data)
- Handles keyboard shortcuts (Enter to send)

#### `Message.jsx`
- Individual message display
- Handles different message types (user, bot, system, error)
- Shows routing information and timestamps

#### `WelcomeMessage.jsx`
- Initial welcome screen
- Usage instructions

#### `LoadingIndicator.jsx`
- Reusable loading spinner
- Used in chat when processing queries

### Custom Hook

#### `useFinancialRAG.js`
- Central state management
- API communication logic
- Business logic for:
  - Document management (upload, list, select)
  - Message handling (send, receive)
  - Loading states
  - Error handling

## 🔄 Data Flow

1. **State Management**: All state is managed in the `useFinancialRAG` hook
2. **Props Passing**: Components receive only the props they need
3. **Event Handling**: Events bubble up through callback props to the hook
4. **API Calls**: All API communication happens in the custom hook

## ✅ Benefits of This Architecture

### Maintainability
- Each component has a single responsibility
- Easy to locate and fix issues
- Clear separation of concerns

### Reusability
- Components can be reused in different contexts
- Self-contained functionality

### Testing
- Each component can be tested in isolation
- Mock props easily for unit tests

### Performance
- Components only re-render when their props change
- Better optimization opportunities

### Developer Experience
- Clear component hierarchy
- Easy to understand data flow
- Consistent patterns

## 🚀 Usage

The refactored application maintains the same functionality but with much cleaner code organization:

```jsx
// Before: Everything in App.jsx (400+ lines)
// After: Clean separation (App.jsx ~50 lines + focused components)

import { useFinancialRAG } from './hooks/useFinancialRAG'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatContainer from './components/ChatContainer'

function App() {
  const ragState = useFinancialRAG()
  
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      <div className="flex-1 flex max-w-6xl mx-auto w-full">
        <Sidebar {...sidebarProps} />
        <ChatContainer {...chatProps} />
      </div>
    </div>
  )
}
```

## 🎯 Key Features Maintained

- ✅ Document upload with progress indicator
- ✅ Real-time document list refresh
- ✅ Document selection for RAG queries
- ✅ Live financial data queries
- ✅ Chat interface with message history
- ✅ Loading states and error handling
- ✅ Responsive design
- ✅ Symbol independence for documents

The refactored code is now much more maintainable and follows React best practices!
