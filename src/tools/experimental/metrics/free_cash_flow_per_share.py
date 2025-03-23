import yfinance as yf


def calculate_free_cash_flow_per_share(stock):
    """
    Calculates free cash flow per share for a given stock ticker.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float: Free cash flow per share, or None if data is unavailable.
    """
    try:

        # Get cash flow data
        cashflow_data = stock.cashflow

        # Get shares outstanding data
        info = stock.info
        shares_outstanding = info["sharesOutstanding"]

        # Calculate free cash flow
        if "Free Cash Flow" in cashflow_data.index:
            free_cash_flow = cashflow_data.loc["Free Cash Flow"].iloc[0]  # Takes the most recent value.

        # Calculate free cash flow per share
        free_cash_flow_per_share = free_cash_flow / shares_outstanding

        return free_cash_flow_per_share

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"  # Apple Inc.
    fcf_per_share = calculate_free_cash_flow_per_share(stock=yf.Ticker(ticker))

    if fcf_per_share is not None:
        print(f"Free cash flow per share for {ticker}: ${fcf_per_share:.2f}")

    ticker2 = "GOOG"  # Alphabet Inc.
    fcf_per_share2 = calculate_free_cash_flow_per_share(stock=yf.Ticker(ticker2))

    if fcf_per_share2 is not None:
        print(f"Free cash flow per share for {ticker2}: ${fcf_per_share2:.2f}")
