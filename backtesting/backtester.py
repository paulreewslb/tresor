import pandas as pd
import datamaster.data_loader as data_loader


class Backtester(object):

    def __init__(self, strategy, freq):
        self._strategy = strategy
        self._freq = freq

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, _strategy):
        self._strategy = _strategy

    @property
    def start(self):
        return self.strategy.start

    @property
    def end(self):
        return self.strategy.end

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, _freq):
        self._freq = _freq

    @property
    def rebal_dates(self):
        return pd.date_range(start=self.start, end=self.end, freq=self.freq)

    @property
    def returns(self):
        prices = data_loader.Price(self.strategy.tickers, start=self.start, end=self.end).adjClose
        return prices/prices.shift(1)-1

    @property
    def pnl(self):
        views = self.strategy.views
        rets = self.returns
        rf = 0  # need to be updated to specify risk free rate
        values = pd.DataFrame(0, index=rets.index, columns=rets.columns)
        cash = pd.Series(0, index=rets.index)
        j = 0
        j_max = len(views.index)
        for i in range(0, len(values.index[1, :])):
            if (values.index[i] < views.index[j]) or (j >= j_max):
                values.iloc[i] = values.iloc[i - 1] * (1 + rets.iloc[i])
                cash[i] = cash[i - 1] * (1 + rf)
            else:
                j = j + 1
                # can set warning here if values.index[i] is far later than views.index[j] say 3 days
                values.iloc[i] = views.loc[values.index[i]]
                cash[i] = cash[i-1]*(1+rf) + sum(values.iloc[i-1]*(1+rets.iloc[i]) - values.iloc[i])

        pnl = values.sum(axis=1) + cash
        return pnl







