import yfinance as yf


def calculate_book_value_growth(stock):
    """
    Calculates the year-over-year book value growth for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        pandas.DataFrame: A DataFrame containing the book value growth, or None if an error occurs.
    """
    try:
        balance_sheet = stock.balance_sheet

        # Extract Total Stockholder Equity
        equity_data = balance_sheet.loc["Stockholders Equity"]

        # Ensure that the data is sorted by date (columns) ascending.
        equity_data = equity_data.sort_index()

        # Calculate year-over-year growth
        growth = equity_data.pct_change(fill_method=None)

        return growth.iloc[-1]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage:


if __name__ == "__main__":
    # Example usage:
    ticker_symbol = "AAPL"  # Replace with the desired stock ticker
    growth_data = calculate_book_value_growth(stock=yf.Ticker(ticker_symbol))

    if growth_data is not None:
        print(f"Book Value Growth for {ticker_symbol}:")
        print(growth_data)
