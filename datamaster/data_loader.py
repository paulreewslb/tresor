"""
this serves as a wrapper for all external data sources.We expect to change data sources frequently. However, the data
structure other modules receive should remain unchanged. All data structure transformations must be handled
within data handler

"""
import pandas_datareader
import pandas as pd
import functools


class DataObj(object):

    def __init__(self, data_source, cache):
        self.data_source = data_source
        self.cache = cache


class Price(DataObj):

    def __init__(self, ticker, start=None, end=None, freq=None, data_source='Yahoo', cache=False):
        super().__init__(data_source, cache)
        assert type(ticker) in [str, list], "Ticker must be type of string or list of string"
        if type(ticker) is list:
            assert functools.reduce(lambda x, y: x&y, [type(item) is str for item in ticker]), \
                "List of tickers must be a list of string!"
        self.ticker = ticker
        if end is None:
            end = pd.datetime.today()
        if start is None:
            start = end - pd.Timedelta(days=365)
        self.start, self.end = pd.to_datetime([start, end])
        self.freq = freq

    @property
    def Close(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Close
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Close\
                    .asfreq(freq=self.freq)

    @property
    def AdjClose(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end)['Adj Close']
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end)['Adj Close']\
                    .asfreq(freq=self.freq)

    @property
    def Open(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Open
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Open.\
                    asfreq(freq=self.freq)

    @property
    def High(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).High
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).High\
                    .asfreq(freq=self.freq)

    @property
    def Low(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Low
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Low\
                    .asfreq(freq=self.freq)

    @property
    def Volumn(self):
        if self.data_source == 'Yahoo':
            if self.freq is None:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Volumn
            else:
                return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).Volumn\
                    .asfreq(freq=self.freq)


if __name__ == '__main__':
    price = Price('AAPL', start='2017-10-01', end='2017-11-01')
    print(price.Close)

