import yfinance as yf


def calculate_working_capital_turnover(stock):
    """
    Calculate the working capital turnover for a given company using Yahoo Finance data.

    Args:
        ticker_symbol (str): The stock ticker symbol of the company.

    Returns:
        float: The working capital turnover ratio, or None if data is unavailable.
    """
    try:
        # Fetch financial data
        financials = stock.financials
        balance_sheet = stock.balance_sheet

        # Get revenue (total revenue from the income statement)
        revenue = financials.loc["Total Revenue"].iloc[0]

        # Get current assets and current liabilities from the balance sheet
        current_assets = balance_sheet.loc["Total Assets"].iloc[0]
        current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0]

        # Calculate working capital
        working_capital = current_assets - current_liabilities

        # Avoid division by zero
        if working_capital == 0:
            return None

        # Calculate working capital turnover
        working_capital_turnover = revenue / working_capital
        return working_capital_turnover

    except Exception as e:
        print(f"Error fetching data or calculating working capital turnover: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"  # Replace with the desired stock ticker
    turnover = calculate_working_capital_turnover(stock=yf.Ticker(ticker))
    if turnover is not None:
        print(f"Working Capital Turnover for {ticker}: {turnover:.2f}")
    else:
        print(f"Could not calculate Working Capital Turnover for {ticker}.")
