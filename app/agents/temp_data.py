import asyncio
from financial_agent import FinancialAgent

agent = FinancialAgent()

async def main():
    response = await agent.answer("Get the income statement", "AAPL", report_type="income statement")
    print("\n=== Financial Report ===\n")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
