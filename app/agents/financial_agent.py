import os
import yfinance as yf
from typing import Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Gemini LLM

# Set your Gemini API Key - FIXED: Use GEMINI_API_KEY to match your .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Add debug line to check if API key is loaded
print(f"DEBUG: GEMINI_API_KEY loaded: {'Yes' if GEMINI_API_KEY else 'No'}")
if GEMINI_API_KEY:
    print(f"DEBUG: API Key starts with: {GEMINI_API_KEY[:10]}...")

# --- TOOL: Fetch Specific Financial Report ---
def fetch_financial_report(symbol: str, report_type: str) -> str:
    """
    Fetches the requested financial report (income statement, balance sheet, or cashflow) for a given stock symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        report_type = report_type.lower()
        if report_type in ["income statement", "income", "profit"]:
            df = ticker.financials
        elif report_type in ["balance sheet", "balance"]:
            df = ticker.balance_sheet
        elif report_type in ["cashflow", "cash flow"]:
            df = ticker.cashflow
        else:
            return "Invalid report type. Please specify 'income statement', 'balance sheet', or 'cashflow'."
        if df.empty:
            return f"No {report_type} data found for {symbol}."
        return df.to_string()
    except Exception as e:
        return f"Error fetching financial report: {e}"

# --- TOOL: Fetch General Company Info ---
def fetch_company_info(symbol: str) -> str:
    """
    Fetches general company info and key financial metrics.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info:
            return "No company info found for this symbol."
        fields = [
            "shortName", "longName", "sector", "industry", "marketCap", "website",
            "dividendYield", "trailingPE", "trailingEps", "forwardEps", "profitMargins"
        ]
        return "\n".join([f"{field}: {info.get(field, 'N/A')}" for field in fields])
    except Exception as e:
        return f"Error fetching company info: {e}"

# --- TOOL: List Available Financial Reports ---
def list_available_reports(symbol: str) -> str:
    """
    Lists which financial reports (income statement, balance sheet, cashflow) are available for the given stock symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        available = []
        if not ticker.financials.empty:
            available.append("income statement")
        if not ticker.balance_sheet.empty:
            available.append("balance sheet")
        if not ticker.cashflow.empty:
            available.append("cashflow")
        if not available:
            return f"No financial reports found for {symbol}."
        return f"Available reports for {symbol}: {', '.join(available)}"
    except Exception as e:
        return f"Error listing available reports: {e}"

# --- Gemini LLM Configuration ---
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=GEMINI_API_KEY
    )
    print("DEBUG: LLM initialized successfully")
except Exception as e:
    print(f"DEBUG: LLM initialization error: {e}")
    llm = None

# --- Tool Functions Dictionary ---
available_tools = {
    "fetch_financial_report": fetch_financial_report,
    "fetch_company_info": fetch_company_info,
    "list_available_reports": list_available_reports
}

# --- Financial Agent Class ---
class FinancialAgent:
    def __init__(self):
        self.llm = llm
        self.tools = available_tools
    
    def _execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a tool function with given parameters."""
        if tool_name in self.tools:
            try:
                return self.tools[tool_name](**kwargs)
            except Exception as e:
                return f"Error executing {tool_name}: {e}"
        else:
            return f"Tool {tool_name} not found. Available tools: {list(self.tools.keys())}"
    
    async def answer(self, question: str, symbol: str, report_type: Optional[str] = None):
        """
        Handles financial queries using LLM + tools.
        If report_type is provided, it's explicitly mentioned in the prompt.
        """
        question = question.strip().capitalize()
        symbol = symbol.upper()
        
        # Create a comprehensive prompt that includes tool descriptions
        tools_description = """
Available tools:
1. fetch_financial_report(symbol, report_type) - Fetch financial statements (income statement, balance sheet, or cashflow)
2. fetch_company_info(symbol) - Fetch general company information and key metrics
3. list_available_reports(symbol) - List which financial reports are available for a stock symbol

You should analyze the user's question and determine which tools to use. Provide a clear and informative response.
"""
        
        if report_type:
            report_type = report_type.lower()
            prompt = f"{tools_description}\n\nUser question: {question} for {symbol} ({report_type})\n\nPlease provide a comprehensive answer using the appropriate tools."
        else:
            prompt = f"{tools_description}\n\nUser question: {question} for {symbol}\n\nPlease provide a comprehensive answer using the appropriate tools."
        
        # For now, let's determine which tool to use based on the question content
        question_lower = question.lower()
        
        if "available" in question_lower or "list" in question_lower:
            result = self._execute_tool("list_available_reports", symbol=symbol)
        elif "company" in question_lower or "info" in question_lower or "general" in question_lower:
            result = self._execute_tool("fetch_company_info", symbol=symbol)
        elif report_type or any(term in question_lower for term in ["income", "balance", "cashflow", "financial", "statement", "report"]):
            if report_type:
                result = self._execute_tool("fetch_financial_report", symbol=symbol, report_type=report_type)
            else:
                # Default to income statement if no specific report type is mentioned
                result = self._execute_tool("fetch_financial_report", symbol=symbol, report_type="income statement")
        else:
            # Default to company info for general questions
            result = self._execute_tool("fetch_company_info", symbol=symbol)
        
        # Use the LLM to provide a more natural response
        final_prompt = f"""
Based on the following data for {symbol}, please provide a clear and informative answer to the user's question: "{question}"

Data:
{result}

Please format your response in a user-friendly way and highlight key insights.
"""
        
        try:
            if self.llm is None:
                return f"LLM not available. Raw data for {symbol}:\n{result}"
            
            response = await self.llm.ainvoke(final_prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            # Fallback to raw data if LLM fails
            print(f"DEBUG: LLM error: {e}")
            return f"Data for {symbol}:\n{result}"

# Create a global instance for backward compatibility
financial_agent_executor = FinancialAgent()