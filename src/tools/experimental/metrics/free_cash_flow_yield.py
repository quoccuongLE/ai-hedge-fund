import yfinance as yf


def calculate_free_cash_flow_yield(stock):
    """
    Calculates the free cash flow yield for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float or None: The free cash flow yield, or None if data is unavailable.
    """
    try:
        # Get free cash flow
        cash_flow = stock.cashflow
        if cash_flow is None or "Free Cash Flow" not in cash_flow.index:
            return None

        free_cash_flow = cash_flow.loc["Free Cash Flow"].iloc[0]

        # Get market cap
        info = stock.info
        if "marketCap" not in info:
            return None
        market_cap = info["marketCap"]

        # Calculate free cash flow yield
        if market_cap == 0:
            return None  # avoid division by zero.
        free_cash_flow_yield = free_cash_flow / market_cap

        return free_cash_flow_yield

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"  # Apple Inc.
    fcf_yield = calculate_free_cash_flow_yield(stock=yf.Ticker(ticker))

    if fcf_yield is not None:
        print(f"Free Cash Flow Yield for {ticker}: {fcf_yield:.4f}")
    else:
        print(f"Could not calculate Free Cash Flow Yield for {ticker}.")
