import pandas as pd
import yfinance as yf

from src.data.models import FinancialMetrics
from src.tools.experimental.metrics import (
    calculate_book_value_growth, calculate_days_sales_outstanding,
    calculate_free_cash_flow_growth, calculate_free_cash_flow_per_share,
    calculate_free_cash_flow_yield, calculate_inventory_turnover,
    calculate_operating_cash_flow_ratio, calculate_operating_cycle,
    calculate_receivables_turnover, calculate_roic,
    calculate_total_debt_to_equity, calculate_working_capital_turnover)


def get_financial_metrics(ticker: str) -> FinancialMetrics:
    """Retrieves financial metrics for a given ticker using yfinance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL" for Apple).

    Returns:
        FinancialMetrics: An instance of the FinancialMetrics class
                          containing the retrieved data.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow

    report_period = "TTM"  # Trailing Twelve Months, generally
    period = "Annual"  # Yahoo finance data often presents annual data

    # Helper function to safely access and convert data
    def get_data(data_source, key, default=None, converter=float):
        try:
            value = data_source.loc[key].iloc[0]
            return converter(value) if pd.notnull(value) else default
        except (KeyError, TypeError, IndexError):
            return default

    def get_info(key, default=None, converter=float):
        try:
            value = info.get(key)
            return converter(value) if value is not None else default
        except TypeError:
            return default

    def calculate_growth(data_source, key, periods=4):  # Default to 4 for annual growth
        """
        Calculate the growth rate of a specific financial metric.

        Args:
            data_source (pd.DataFrame): DataFrame containing the financial data.
            key (str): The key of the metric to calculate growth for.
            periods (int): The number of periods to calculate growth over (e.g., 4 for annual).

        Returns:
            float: The growth rate, or None if data is insufficient.
        """
        try:
            if data_source is None or key not in data_source.index:
                return None

            # Ensure data_source is treated as a DataFrame
            if not isinstance(data_source, pd.DataFrame):
                return None

            values = data_source.loc[key]
            if len(values) > periods:
                current_value = values.iloc[0]
                previous_value = values.iloc[periods]
                if pd.notnull(current_value) and pd.notnull(previous_value) and previous_value != 0:
                    return (current_value - previous_value) / previous_value
                else:
                    return None
            else:
                return None
        except (TypeError, IndexError, KeyError):
            return None

    try:
        currency = info.get("currency")
    except:
        currency = None

    market_cap = get_info("marketCap")
    enterprise_value = get_info("enterpriseValue")
    price_to_earnings_ratio = get_info("trailingPE")
    price_to_book_ratio = get_info("priceToBook")
    price_to_sales_ratio = get_info("trailingPriceToSales")
    enterprise_value_to_ebitda_ratio = get_info("enterpriseToEbitda")
    enterprise_value_to_revenue_ratio = get_info("enterpriseToRevenue")
    peg_ratio = get_info("pegRatio")

    # Gross Margin Calculation
    if financials is not None and "Gross Profit" in financials.index and "Total Revenue" in financials.index and get_data(financials, "Total Revenue") != 0:
        gross_margin = get_data(financials, "Gross Profit") / get_data(financials, "Total Revenue")
    else:
        gross_margin = None
    operating_margin = get_data(financials, "Operating Income") / get_data(financials, "Total Revenue") if financials is not None and "Operating Income" in financials.index and "Total Revenue" in financials.index and get_data(financials, "Total Revenue") != 0 else None
    net_margin = get_data(financials, "Net Income") / get_data(financials, "Total Revenue") if financials is not None and "Net Income" in financials.index and "Total Revenue" in financials.index and get_data(financials, "Total Revenue") != 0 else None

    return_on_equity = get_info("returnOnEquity")
    return_on_assets = get_info("returnOnAssets")
    return_on_invested_capital = calculate_roic(stock)

    asset_turnover = get_data(financials, "Total Revenue") / get_data(balance_sheet, "Total Assets") if financials is not None and balance_sheet is not None and "Total Revenue" in financials.index and "Total Assets" in balance_sheet.index and get_data(balance_sheet, "Total Assets") != 0 else None

    # Yahoo finance does not directly provide inventory or receivables turnover.
    inventory_turnover = calculate_inventory_turnover(stock)
    receivables_turnover = calculate_receivables_turnover(stock)
    days_sales_outstanding = calculate_days_sales_outstanding(stock)
    operating_cycle = calculate_operating_cycle(stock)
    working_capital_turnover = calculate_working_capital_turnover(stock)

    current_ratio = get_data(balance_sheet, "Total Current Assets") / get_data(balance_sheet, "Current Liabilities") if balance_sheet is not None and "Total Current Assets" in balance_sheet.index and "Total Current Liabilities" in balance_sheet.index and get_data(balance_sheet, "Current Liabilities") != 0 else None

    quick_ratio = (get_data(balance_sheet, "Total Current Assets") - get_data(balance_sheet, "Inventory", 0)) / get_data(balance_sheet, "Current Liabilities") if balance_sheet is not None and "Total Current Assets" in balance_sheet.index and "Inventory" in balance_sheet.index and "Current Liabilities" in balance_sheet.index and get_data(balance_sheet, "Current Liabilities") != 0 else None

    cash_ratio = get_data(balance_sheet, "Cash") / get_data(balance_sheet, "Current Liabilities") if balance_sheet is not None and "Cash" in balance_sheet.index and "Current Liabilities" in balance_sheet.index and get_data(balance_sheet, "Current Liabilities") != 0 else None
    operating_cash_flow_ratio = calculate_operating_cash_flow_ratio(stock)

    debt_to_equity = get_info("debtToEquity")
    # Yahoo Finance provides total debt to equity. Debt to assets is not provided.
    debt_to_assets = calculate_total_debt_to_equity(stock)
    interest_coverage = get_info("interestCoverage")

    revenue_growth = calculate_growth(financials, "Total Revenue")
    earnings_growth = calculate_growth(financials, "Net Income")
    # Yahoo finance does not provide book value, growth is not directly available.
    book_value_growth = calculate_book_value_growth(stock)
    earnings_per_share_growth = calculate_growth(financials, "Basic EPS")
    # Free cash flow growth is not directly available
    free_cash_flow_growth = calculate_free_cash_flow_growth(stock)
    operating_income_growth = calculate_growth(financials, "Operating Income")
    ebitda_growth = calculate_growth(financials, "EBITDA")
    payout_ratio = get_info("payoutRatio")
    earnings_per_share = get_info("epsForward")
    book_value_per_share = get_info("bookValue")
    # Free cash flow per share is not available
    free_cash_flow_per_share = calculate_free_cash_flow_per_share(stock)

    free_cash_flow_yield = calculate_free_cash_flow_yield(stock)

    return FinancialMetrics(
        ticker=ticker,
        report_period=report_period,
        period=period,
        currency=currency,
        market_cap=market_cap,
        enterprise_value=enterprise_value,
        price_to_earnings_ratio=price_to_earnings_ratio,
        price_to_book_ratio=price_to_book_ratio,
        price_to_sales_ratio=price_to_sales_ratio,
        enterprise_value_to_ebitda_ratio=enterprise_value_to_ebitda_ratio,
        enterprise_value_to_revenue_ratio=enterprise_value_to_revenue_ratio,
        free_cash_flow_yield=free_cash_flow_yield,  # Not directly available
        peg_ratio=peg_ratio,
        gross_margin=gross_margin,
        operating_margin=operating_margin,
        net_margin=net_margin,
        return_on_equity=return_on_equity,
        return_on_assets=return_on_assets,
        return_on_invested_capital=return_on_invested_capital,
        asset_turnover=asset_turnover,
        inventory_turnover=inventory_turnover,
        receivables_turnover=receivables_turnover,
        days_sales_outstanding=days_sales_outstanding,
        operating_cycle=operating_cycle,
        working_capital_turnover=working_capital_turnover,
        current_ratio=current_ratio,
        quick_ratio=quick_ratio,
        cash_ratio=cash_ratio,
        operating_cash_flow_ratio=operating_cash_flow_ratio,
        debt_to_equity=debt_to_equity,
        debt_to_assets=debt_to_assets,
        interest_coverage=interest_coverage,
        revenue_growth=revenue_growth,
        earnings_growth=earnings_growth,
        book_value_growth=book_value_growth,
        earnings_per_share_growth=earnings_per_share_growth,
        free_cash_flow_growth=free_cash_flow_growth,
        operating_income_growth=operating_income_growth,
        ebitda_growth=ebitda_growth,
        payout_ratio=payout_ratio,
        earnings_per_share=earnings_per_share,
        book_value_per_share=book_value_per_share,
        free_cash_flow_per_share=free_cash_flow_per_share,
    )


if __name__ == "__main__":
    # Example usage:
    ticker_symbol = "AAPL"  # Replace with the desired stock ticker
    metrics = get_financial_metrics(ticker_symbol)
    print(metrics)  # Output the data as a formatted JSON string
