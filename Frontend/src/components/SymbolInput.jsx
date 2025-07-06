// Symbol input component
import React from 'react'

const SymbolInput = ({ symbol, setSymbol }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Stock Symbol
      </label>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="e.g., AAPL, MSFT"
      />
    </div>
  )
}

export default SymbolInput
