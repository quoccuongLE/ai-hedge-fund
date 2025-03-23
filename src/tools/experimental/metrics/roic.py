import yfinance as yf
import pandas as pd


def calculate_roic(stock: str) -> float | None:
    """
    Calculates the Return on Invested Capital (ROIC) for a given stock ticker using yfinance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        float | None: The calculated ROIC, or None if the data is not available
                      or if an error occurs during calculation.
    """
    try:
        # Get the income statement and balance sheet
        income_statement = stock.financials
        balance_sheet = stock.balance_sheet

        if income_statement is None or balance_sheet is None:
            return None

        # Extract the necessary values
        net_income = income_statement.loc["Net Income"].iloc[0]
        total_debt = balance_sheet.loc["Total Debt"].iloc[0]
        total_equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

        # Check for missing values
        if pd.isna(net_income) or pd.isna(total_debt) or pd.isna(total_equity):
            return None

        # Calculate invested capital
        invested_capital = total_debt + total_equity

        if invested_capital == 0:
            return None  # Avoid division by zero

        # Calculate ROIC
        roic = net_income / invested_capital
        return roic

    except Exception as e:
        print(f"Error calculating ROIC for {stock}: {e}")
        return None


if __name__ == "__main__":
    ticker_symbol = "AAPL"  # Example ticker
    roic = calculate_roic(stock=yf.Ticker(ticker_symbol))

    if roic is not None:
        print(f"The ROIC for {ticker_symbol} is: {roic:.2f}")
    else:
        print(f"Could not calculate ROIC for {ticker_symbol}.")
