import numpy as _np
import pandas as _pd


class RiskModel(object):

    def __init__(self, component_returns, index_returns, ret_type):
        """
        initialization of RiskModel class. The initialization also pre-compute x*y and x2 at each time so the results
        can be used for fast rolling computation
        :param component_returns: a df containing returns of component stocks, date as index
        :param index_returns: a series containing index returns for beta computation, date as index
        """

        assert isinstance(component_returns, _pd.DataFrame), "component_returns should be a dataframe"
        assert isinstance(index_returns, _pd.Series), "index_returns should be a series"
        assert set(index_returns.index) == set(component_returns.index), "date index must agree"
        assert ret_type in ['simple', 'log'], "invalid return type"

        self.__component_returns__ = component_returns
        self.__index_returns__ = index_returns
        self.__ret_type__ = ret_type

    @property
    def get_comopent_returns(self):

        return self.__component_returns__

    @property
    def get_index_returns(self):

        return self.__index_returns__

    def simple_to_log_conversion(self):

        assert self.__ret_type__ == 'simple', "the original return type should be simple"
        f = lambda x: _np.log(1 + x)
        log_comp_ret = self.__component_returns__.applymap(f)
        log_idx_ret = self.__index_returns__.apply(f)

        return log_idx_ret, log_comp_ret

    def log_to_simple_conversion(self):

        assert self.__ret_type__ == 'log', "the original return type should be log"
        f = lambda x: _np.exp(x) - 1
        simple_comp_ret = self.__component_returns__.applymap(f)
        simple_idx_ret = self.__index_returns__.apply(f)

        return simple_idx_ret, simple_comp_ret

    def get_rolling_ret(self, rolling_window):

        if self.__ret_type__ == 'simple':
            comp_rolling_ret = self.__component_returns__.rolling(rolling_window).apply(lambda x: _np.prod(1 + x)) - 1
            idx_rolling_ret = self.__index_returns__.rolling(rolling_window).apply(lambda x: _np.prod(1 + x)) - 1
        else:
            comp_rolling_ret = self.__component_returns__.rolling(rolling_window).sum()
            idx_rolling_ret = self.__index_returns__.rolling(rolling_window).sum()

        return idx_rolling_ret.iloc[(rolling_window - 1):], comp_rolling_ret.iloc[(rolling_window - 1):]

    @classmethod
    def get_ewma_weights(cls, df, lookback_window, decay):

        assert type(df) in [_pd.DataFrame, _pd.Series], "df should be a dataframe or series"
        assert decay > 0 and decay <= 1, " 0 < decay <= 1"

        idx = df.index
        weights = _np.array(map(lambda x: decay ** (len(idx) - x - 1), range(len(idx))))

        weights = _pd.Series(weights, index=idx, name='ewma_weight')
        sum_weight = weights.rolling(lookback_window).sum()

        return weights, sum_weight

    def get_realized_beta(self, lookback_window, rolling_ret_window=1, decay=1):

        idx_ret, comp_ret = self.get_rolling_ret(rolling_ret_window)

        prod = comp_ret.multiply(idx_ret, axis='index')
        idx_ret_sq = idx_ret ** 2

        weights, sum_weight = self.get_ewma_weights(idx_ret_sq, lookback_window, decay)

        idx_ret_sq = idx_ret_sq.multiply(weights, axis='index')
        prod = prod.multiply(weights, axis='index')

        numerator = prod.rolling(lookback_window).sum()
        denominator = idx_ret_sq.rolling(lookback_window).sum()

        return numerator.div(denominator, axis='index')

    def get_realized_vol(self, lookback_window, rolling_ret_window=1, decay=1):

        idx_ret, comp_ret = self.get_rolling_ret(rolling_ret_window)

        idx_wgt, idx_sum_wgt = self.get_ewma_weights(idx_ret, lookback_window, decay)
        comp_wgt, comp_sum_wgt = self.get_ewma_weights(comp_ret, lookback_window, decay)

        res_idx = _np.sqrt((idx_ret ** 2).multiply(idx_wgt, axis='index').rolling(lookback_window).sum().
                           div(idx_sum_wgt, axis='index') * 260 / rolling_ret_window)
        res_comp = _np.sqrt((comp_ret.applymap(lambda x: x**2)).multiply(comp_wgt, axis='index').
                            rolling(lookback_window).sum().div(comp_sum_wgt, axis='index') * 260 / rolling_ret_window)

        return res_idx, res_comp

    def get_realized_corr(self, lookback_window, rolling_ret_window=1):

        idx_ret, comp_ret = self.get_rolling_ret(rolling_ret_window)

        df_all = _pd.concat([idx_ret, comp_ret], axis=1)

        l = []
        for date in df_all.index[:-lookback_window]:
            # Note loc includes the last item, index excludes last item
            temp = df_all.loc[date: date + _pd.offsets.BDay(lookback_window - 1)].corr().reset_index()
            temp.rename(columns={'index': 'ticker'}, inplace=True)
            temp['date'] = date
            l.append(temp)
        res = _pd.concat(l)
        res.set_index(['date', 'ticker'], inplace=True)

    def get_ex_ante_vol(self, decay, lookback_window):

        pass

    def get_ex_ante_beta(self, decay, lookback):

        pass
