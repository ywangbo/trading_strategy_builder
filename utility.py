
import yfinance as yf
import pandas as pd


def get_next_earnings_date(symbol):
    stock = yf.Ticker(symbol)
    earnings = stock.get_earnings_dates()

    if earnings is None or earnings.empty:
        return "#N/A"
    
    today = pd.Timestamp.today(tz=earnings.index.tz)
    future_earnings = earnings.index[pd.to_datetime(earnings.index) > today]
    if not future_earnings.empty:
        nearest_earnings_date = future_earnings.min()
        return nearest_earnings_date
    else:
        return "#N/A"


def get_put_call_ratio(symbol):
    options = yf.Ticker(symbol).options

    # Filter for available expirations and use the first one
    expiration = options[0]
    chain = yf.Ticker(symbol).option_chain(expiration)
    put_call_ratio = chain.put_open_interest.sum() / chain.call_open_interest.sum()

    return put_call_ratio