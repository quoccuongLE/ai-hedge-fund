import yfinance as yf
import pandas as pd


def calculate_days_sales_outstanding(stock):
    """
    Calculates Days Sales Outstanding (DSO) for a given stock ticker using Yahoo Finance data.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float or str: The DSO, or an error message if data is unavailable.
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

        # Extract net sales
        net_sales = income_statement.loc["Total Revenue"].iloc[0]

        # Extract accounts receivable.
        accounts_receivable = balance_sheet.loc["Accounts Receivable"]
        if accounts_receivable.empty:
            return "Accounts receivable data not available."

        if len(accounts_receivable) > 1:
            avg_receivables = accounts_receivable.iloc[0:2].mean()  # average of the 2 most recent years
        else:
            avg_receivables = accounts_receivable.iloc[0]

        # Calculate DSO
        if net_sales == 0:
            return "Net Sales is zero, DSO cannot be calculated"

        dso = (avg_receivables / net_sales) * 365

        return dso

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Example usage:
    ticker = "AAPL"
    dso = calculate_days_sales_outstanding(stock=yf.Ticker(ticker))

    if isinstance(dso, (int, float)):
        print(f"Days Sales Outstanding (DSO) for {ticker}: {dso:.2f} days")
    else:
        print(dso)
