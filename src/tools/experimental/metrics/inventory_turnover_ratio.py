import yfinance as yf
import pandas as pd


def calculate_inventory_turnover(stock: str) -> float | None:
    """
    Calculates the inventory turnover ratio for a given stock ticker using yfinance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float | None: The calculated inventory turnover ratio, or None if the data is not available
                      or if an error occurs during calculation.
    """
    try:
        
        # Get the income statement and balance sheet
        income_statement = stock.financials  # Annual data
        balance_sheet = stock.balance_sheet  # Annual data

        if income_statement is None or balance_sheet is None:
            return None

        # Extract the necessary values
        cost_of_goods_sold = income_statement.loc["Cost Of Revenue"].iloc[0]
        # Average inventory is (beginning inventory + ending inventory) / 2
        # For annual data, we can use the inventory from the beginning and end of the year.
        # Assuming the first entry in the balance sheet is the beginning of the period
        # and the last entry is the end of the period.  This is a simplification.
        beginning_inventory = balance_sheet.loc["Inventory"].iloc[1] if "Inventory" in balance_sheet.index else None
        ending_inventory = balance_sheet.loc["Inventory"].iloc[0] if "Inventory" in balance_sheet.index else None

        # Check for missing values
        if pd.isna(cost_of_goods_sold) or beginning_inventory is None or ending_inventory is None:
            return None

        average_inventory = (beginning_inventory + ending_inventory) / 2

        if average_inventory == 0:
            return None  # Avoid division by zero

        # Calculate inventory turnover
        inventory_turnover = cost_of_goods_sold / average_inventory
        return inventory_turnover

    except Exception as e:
        print(f"Error calculating inventory turnover for {stock}: {e}")
        return None


if __name__ == "__main__":
    ticker_symbol = "AAPL"  # Example ticker
    inventory_turnover = calculate_inventory_turnover(stock=yf.Ticker(ticker_symbol))

    if inventory_turnover is not None:
        print(f"The inventory turnover ratio for {ticker_symbol} is: {inventory_turnover:.2f}")
    else:
        print(f"Could not calculate inventory turnover ratio for {ticker_symbol}.")
