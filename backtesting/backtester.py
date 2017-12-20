import pandas as pd
import datamaster.data_loader as data_loader


class Backtester(object):

    def __init__(self, strategy, freq, start=None, end=None):
        self._strategy = strategy
        self._freq = freq
        self.start = start
        self.end = end

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, _strategy):
        self._strategy = _strategy

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, _start):
        if _start is None:
            self._start = self.strategy.start
        else:
            if pd.to_datetime(_start) >= pd.to_datetime(self.strategy.start):
                self._start = _start
            else:
                self._start = self.strategy.start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, _end):
        if _end is None:
            self._end = self.strategy.end
        else:
            if pd.to_datetime(_end) >= pd.to_datetime(self.strategy.end):
                self._end = self.strategy.end
            else:
                self._end = _end

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, _freq):
        self._freq = _freq

    @property
    def rebal_dates(self):
        init_date = max(self.strategy.views.index[0], pd.to_datetime(self.start))
        return pd.date_range(init_date, init_date).\
            union(pd.date_range(start=self.start, end=self.end, freq=self.freq))

    @property
    def returns(self):
        prices = data_loader.Price(self.strategy.tickers, start=self.start, end=self.end).adjClose
        return prices/prices.shift(1)-1

    @property
    def views(self):
        return self.strategy.views.reindex(self.rebal_dates, method='ffill')

    @property
    def pnl(self):
        rets = self.returns
        views = self.views
        rf = 0  # need to be updated to specify risk free rate
        positions = pd.DataFrame(0, index=rets.index, columns=rets.columns)
        pnl = pd.Series(0, index=rets.index)
        j = 0
        j_max = len(self.rebal_dates)
        for i in range(0, len(positions)):
            if j >= j_max:
                if i == 0: continue
                pnl.iloc[i] = pnl.iloc[i-1] + sum(positions.iloc[i-1]*rets.iloc[i])
                positions.iloc[i] = positions.iloc[i-1] * (1 + rets.iloc[i])
            elif positions.index[i] < views.index[j]:
                if i == 0: continue
                pnl.iloc[i] = pnl.iloc[i-1] + sum(positions.iloc[i-1]*rets.iloc[i])
                positions.iloc[i] = positions.iloc[i-1] * (1 + rets.iloc[i])
            else:
                # can set warning here if values.index[i] is far later than views.index[j] say 3 days
                if i == 0:
                    positions.iloc[i] = views.iloc[j]
                else:
                    pnl.iloc[i] = pnl.iloc[i-1] + sum(positions.iloc[i-1]*rets.iloc[i])
                    positions.iloc[i] = (1 + pnl.iloc[i]) * views.iloc[j]
                j = j+1

        return pnl, positions







