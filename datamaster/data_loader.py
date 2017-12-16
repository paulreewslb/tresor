"""
this serves as a wrapper for all external data sources.We expect to change data sources frequently. However, the data
structure other modules receive should remain unchanged. All data structure transformations must be handled
within data handler

"""
import pandas_datareader
import pandas as pd
from datamaster.json_loader import get_json_data


class DataObj(object):

    __data__ = {}

    def __init__(self, data_source, cache):
        self.data_source = data_source
        self.cache = cache
        self.__data__[self.__class__.__name__] = {}

    def get_data(self, *args):
        if self.cache is True:
            key = tuple(args)
            try:
                data = self.__data__[self.__class__.__name__][key]
            except KeyError:
                data = self._get_data()
                self.__data__[self.__class__.__name__][key] = data
        if self.cache is False:
            data = self._get_data()
        return data

    def _get_data(self):
        raise Exception("Must be implemented in inherited class!")


class Price(DataObj):

    def __init__(self, ticker, start=None, end=None, freq=None, data_source='yahoo', cache=False):
        super().__init__(data_source, cache)
        if type(ticker) is not str:
            ticker = list(ticker)
        self.ticker = ticker
        if end is None:
            end = pd.datetime.today()
        if start is None:
            start = end - pd.Timedelta(days=365)
        self.start, self.end = pd.to_datetime([start, end])
        self.freq = freq
        self.data = self.get_data(data_source, tuple(self.ticker), start, end)

    def _get_data(self):
        if self.data_source == 'yahoo':
            return pandas_datareader.data.DataReader(self.ticker, 'yahoo', self.start, self.end).iloc[:,::-1,:]
        else:
            pass  # code for other data source

    @property
    def close(self):
        if self.freq is None:
            return self.data.Close
        else:
            return self.data.Close.asfreq(self.freq)

    @property
    def adjClose(self):
        if self.freq is None:
            return self.data['Adj Close']
        else:
            return self.data['Adj Close'].asfreq(self.freq)

    @property
    def open(self):
        if self.freq is None:
            return self.data.Open
        else:
            return self.data.Open.asfreq(self.freq)

    @property
    def high(self):
        if self.freq is None:
            return self.data.High
        else:
            return self.data.High.asfreq(self.freq)

    @property
    def low(self):
        if self.freq is None:
            return self.data.Low
        else:
            return self.data.Low.asfreq(self.freq)

    @property
    def volume(self):
        if self.freq is None:
            return self.data.Volume
        else:
            return self.data.Volume.asfreq(self.freq)


class Industry(DataObj):

    def __init__(self, name, data_source='GICS.json', cache=False):
        super().__init__(data_source, cache)
        self.name = name
        self.data = self.get_data(data_source, name)

    def _get_data(self):
        if self.data_source == 'GICS.json':
            if self.name.startswith('SP500'):
                return pd.DataFrame.from_dict(
                    get_json_data('industry_source', 'GICS')['SP500'], orient='index')
            else:
                pass # code for other industry name
        else:
            pass  # code for other data source

    @property
    def list(self):
        if self.data_source == 'GICS.json':
            if self.name == 'SP500':
                return list(self.data.index)
            else:  # item name should be 'SP500_Sector_SubIndustry':
                subs = self.name.split('_')
                if len(subs) == 2:
                    return list(self.data[self.data['GICS Sector']==subs[1]].index)
                elif len(subs) == 3:
                    return list(self.data[(self.data['GICS Sector']==subs[1])&
                                          (self.data['GICS Sub Industry']==subs[2])].index)
                else:
                    raise Exception("Invalid Item Name for Industry List")

    def map(self, level):
        return self.data[level]


if __name__ == '__main__':
    price = Price(['AAPL','AMZN'], start='2017-03-01', end='2017-11-01', cache=True)
    print(price.close)

