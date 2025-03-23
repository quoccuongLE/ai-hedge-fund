import yfinance as yf
import pandas as pd


def calculate_operating_cycle(stock):
    """
    Calculates the Operating Cycle for a given stock ticker using Yahoo Finance data.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float or str: The Operating Cycle (in days), or an error message if data is unavailable.
    """
    try:
        # Get income statement data
        income_statement = stock.financials
        if income_statement.empty:
            return "Income statement data not available."

        # Get balance sheet data
        balance_sheet = stock.balance_sheet
        if balance_sheet.empty:
            return "Balance sheet data not available."

        # Extract necessary data
        net_sales = income_statement.loc["Total Revenue"].iloc[0]

        # Handle potential variations in cost of goods sold key
        if "Cost Of Goods Sold" in income_statement.index:
            cost_of_goods_sold = income_statement.loc["Cost Of Goods Sold"].iloc[0]
        elif "Cost Of Revenue" in income_statement.index:
            cost_of_goods_sold = income_statement.loc["Cost Of Revenue"].iloc[0]
        else:
            return "Cost of Goods Sold/Revenue data not available."

        inventory = balance_sheet.loc["Inventory"]
        accounts_receivable = balance_sheet.loc["Accounts Receivable"]

        # Handle missing data
        if inventory.empty:
            return "Inventory data not available."
        if accounts_receivable.empty:
            return "Accounts receivable data not available."
        if cost_of_goods_sold == 0:
            return "Cost of Goods Sold/Revenue is zero, Inventory days cannot be calculated"
        if net_sales == 0:
            return "Net Sales is zero, Days sales outstanding cannot be calculated"

        # Calculate average inventory and accounts receivable
        if len(inventory) > 1:
            avg_inventory = inventory.iloc[0:2].mean(skipna=True)
        else:
            avg_inventory = inventory.iloc[0]

        if len(accounts_receivable) > 1:
            avg_receivables = accounts_receivable.iloc[0:2].mean()
        else:
            avg_receivables = accounts_receivable.iloc[0]

        # Calculate Inventory Days and Days Sales Outstanding (DSO)
        inventory_days = (avg_inventory / cost_of_goods_sold) * 365
        dso = (avg_receivables / net_sales) * 365

        # Calculate Operating Cycle
        operating_cycle = inventory_days + dso

        return operating_cycle

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    ticker = "AAPL"
    stock = yf.Ticker(ticker)
    operating_cycle = calculate_operating_cycle(stock)

    if isinstance(operating_cycle, (int, float)):
        print(f"Operating Cycle for {ticker}: {operating_cycle:.2f} days")
    else:
        print(operating_cycle)
