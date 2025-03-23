import yfinance as yf


def calculate_free_cash_flow_growth(stock):
    """
    Calculates the free cash flow growth for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        period (str): The time period for which to fetch financial data (e.g., "5y", "10y").

    Returns:
        float or None: The free cash flow growth percentage, or None if data is unavailable or an error occurs.
    """
    try:
        cashflow = stock.cashflow

        if cashflow.empty:
            return None  # No cash flow data available

        # Transpose the DataFrame to easily access data by year
        cashflow = cashflow.transpose()

        # Extract free cash flow data. It may be named differently.
        fcf_columns = [col for col in cashflow.columns if "Free Cash Flow" in col]

        if not fcf_columns:
            return None  # Free cash flow column not found

        fcf_column = fcf_columns[0]  # Use the first matching column

        fcf = cashflow[fcf_column].dropna()  # Drop NaN values

        if len(fcf) < 2:
            return None  # Not enough data points to calculate growth

        # Calculate growth
        first_fcf = fcf.iloc[0]
        last_fcf = fcf.iloc[-1]

        if first_fcf == 0:
            return None  # Avoid division by zero

        # growth = ((last_fcf - first_fcf) / abs(first_fcf)) * 100
        growth = (last_fcf - first_fcf) / abs(first_fcf)

        return growth

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    growth = calculate_free_cash_flow_growth(stock=yf.Ticker(ticker))

    if growth is not None:
        print(f"Free cash flow growth for {ticker}: {growth:.2f}%")
    else:
        print(f"Could not calculate free cash flow growth for {ticker}.")
