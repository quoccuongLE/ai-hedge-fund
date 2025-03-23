import yfinance as yf


def calculate_total_debt_to_equity(stock):
    """
    Calculates the total debt to equity ratio for a given stock ticker using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float: The total debt to equity ratio, or None if data is unavailable or an error occurs.
    """
    try:
        balance_sheet = stock.balance_sheet

        if balance_sheet.empty:
            return None

        total_debt = balance_sheet.loc["Total Debt"].iloc[0]  # gets the value in the first column, which is the most recent.
        total_stockholder_equity = balance_sheet.loc["Stockholders Equity"].iloc[0]  # gets the value in the first column, which is the most recent.

        if total_stockholder_equity == 0:
            return float("inf")  # Handle division by zero

        debt_to_equity = total_debt / total_stockholder_equity
        return debt_to_equity

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    ticker = "AAPL"
    debt_equity_ratio = calculate_total_debt_to_equity(stock=yf.Ticker(ticker))

    if debt_equity_ratio is not None:
        print(f"Total Debt to Equity Ratio for {ticker}: {debt_equity_ratio}")

    ticker2 = "GOOG"
    debt_equity_ratio2 = calculate_total_debt_to_equity(ticker2)

    if debt_equity_ratio2 is not None:
        print(f"Total Debt to Equity Ratio for {ticker2}: {debt_equity_ratio2}")
