import yfinance as yf
import pandas as pd


def calculate_receivables_turnover(stock):
    """
    Calculates receivables turnover for a given stock ticker using Yahoo Finance data.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float or str: The receivables turnover ratio, or an error message if data is unavailable.
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
        net_sales = income_statement.loc["Total Revenue"].iloc[0]  # most recent year

        # Extract accounts receivable. Use the average of beginning and ending period.
        accounts_receivable = balance_sheet.loc["Accounts Receivable"]
        if accounts_receivable.empty:
            return "Accounts receivable data not available."

        if len(accounts_receivable) > 1:
            avg_receivables = accounts_receivable.iloc[0:2].mean()  # average of the 2 most recent years
        else:
            avg_receivables = accounts_receivable.iloc[0]

        # Calculate receivables turnover
        receivables_turnover = net_sales / avg_receivables

        return receivables_turnover

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Example usage:
    ticker = "AAPL"
    turnover = calculate_receivables_turnover(stock=yf.Ticker(ticker))

    if isinstance(turnover, (int, float)):
        print(f"Receivables Turnover for {ticker}: {turnover:.2f}")
    else:
        print(turnover)
