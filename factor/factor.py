from factor.config_loader import get_config_item
import signal.signal_loader as signal_loader
import datamaster.data_loader as data_loader
import transform.transforms.Tfuncs as Tfuncs
import pandas as pd
from backtesting.backtester import Backtester

class Factor(object):

    def __init__(self, factor_name=None, start=None, end=None, factor_settings_override=None):
        self._factor_name = factor_name
        self._start = start
        self._end = end
        self._views = None
        if factor_name is not None:
            self._factor_settings = self._get_factor_settings()
        else:
            self._factor_settings = dict()
        if factor_settings_override is not None:
            self._factor_settings.update(factor_settings_override)

    def _get_factor_settings(self):
        return get_config_item("factor_settings", self._factor_name)

    def _clear(self):
        self._views = None

    @property
    def factor_name(self):
        return self._factor_name

    @factor_name.setter
    def factor_name(self, _factor_name):
        self._clear()
        self._factor_name = _factor_name

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, _start):
        self._clear()
        self._start = _start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, _end):
        self._clear()
        self._end = _end

    @property
    def factor_settings(self):
        return self._factor_settings

    def update(self, factor_settings_updates):
        self._clear()
        self._factor_settings.update(factor_settings_updates)

    @property
    def tickers(self):
        universe = self.factor_settings['Universe']
        assert type(universe) is list or str, "type of universe should be str or list"
        if type(universe) is not list:
            universe = [universe]
        ticker_list = []
        for u in universe:
            ticker_list.extend(data_loader.Industry(u).list)
        assert len(ticker_list) == len(set(ticker_list)), \
            "Universes containing common stocks are not supposed to be merged!"
        return ticker_list

    @property
    def views(self):
        if self._views is None:
            if 'Signal' in self.factor_settings:
                signal_func = getattr(signal_loader, self.factor_settings['Signal'])
                signal_params = self.factor_settings['Signal_Params']
                outputs = signal_func(self.tickers, self.start, self.end, **signal_params)
            if 'Composites' in self.factor_settings:
                outputs = None # code to be updated for composite factor
            views = pd.DataFrame(index=outputs.index, columns=outputs.columns)
            TSeq = self.factor_settings['TSeq']
            for t in outputs.index:
                output = outputs.loc[t].copy()
                for Tfunc_name in TSeq:
                    _input = output
                    Tfunc = getattr(Tfuncs, Tfunc_name)
                    output, auxiliary = Tfunc(_input, **self.factor_settings)
                views.loc[t] = output
            self._views = views
        return self._views

    def backtest(self, freq, start=None, end=None):
        backtester = Backtester(self, freq, start, end)
        return backtester.pnl




