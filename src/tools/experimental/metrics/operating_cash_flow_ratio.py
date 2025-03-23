import yfinance as yf


def calculate_operating_cash_flow_ratio(stock):
    """
    Calculates the operating cash flow ratio for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float or None: The operating cash flow ratio, or None if data is unavailable or an error occurs.
    """
    try:
        cash_flow = stock.cashflow
        balance_sheet = stock.balance_sheet

        if cash_flow.empty or balance_sheet.empty:
            return None

        # Extract necessary values, handling potential KeyError
        try:
            operating_cash_flow = cash_flow.loc["Operating Cash Flow"].iloc[0]
            current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0]
        except KeyError:
            return None

        # Calculate the ratio
        if current_liabilities != 0:
            operating_cash_flow_ratio = operating_cash_flow / current_liabilities
            return operating_cash_flow_ratio
        else:
            return None  # Avoid division by zero

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    ratio = calculate_operating_cash_flow_ratio(stock=yf.Ticker(ticker))

    if ratio is not None:
        print(f"Operating Cash Flow Ratio for {ticker}: {ratio}")
    else:
        print(f"Could not calculate Operating Cash Flow Ratio for {ticker}.")
