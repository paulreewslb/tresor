import pandas as pd
from datamaster.data_loader import Price

def p_xy(tickers, start, end, x, y, price_item='adjClose', data_source='yahoo'):
    """

    :param date:
    :param tickers: List of tickers
    :return: return of price over x month ago to y month ago
    """
    start = pd.to_datetime(start) - pd.DateOffset(months=y) - pd.tseries.offsets.BDay(1)
    prices = getattr(Price(tickers, start=start, end=end, data_source=data_source), price_item)
    idx = prices.index
    idx_x = idx - pd.DateOffset(months=x) - pd.tseries.offsets.BDay(1)
    idx_y = idx - pd.DateOffset(months=y) - pd.tseries.offsets.BDay(1)
    p_x = pd.DataFrame(prices.reindex(idx_x).values, index=idx)
    p_y = pd.DataFrame(prices.reindex(idx_y).values, index=idx)
    return (p_x/p_y).dropna(axis=0, how='all')

