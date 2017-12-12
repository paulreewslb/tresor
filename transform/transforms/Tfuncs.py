import numpy as _np
import pandas as _pd
import statsmodels.api as _sm_api
import datamaster.data_loader as data_loader
import transform.transforms.utils as utils


def trim_percentile(series, *args, **kwargs):
    lower_percentile = 0.01 if 'lower_percentile' not in kwargs else kwargs['lower_percentile']
    upper_percentile = 0.99 if 'upper_percentile' not in kwargs else kwargs['upper_percentile']
    if 'Groupby_Item' in kwargs:
        groupby_item = kwargs['Groupby_Item']
        grouping = data_loader.Industry(kwargs['Universe']).map(groupby_item).reindex(series.index)
        lower_bound = series.groupby(grouping).transform(lambda x:_np.percentile(x, 100 * lower_percentile))
        upper_bound = series.groupby(grouping).transform(lambda x:_np.percentile(x, 100 * upper_percentile))
    else:
        lower_bound = _np.percentile(series, lower_percentile)
        upper_bound = _np.percentile(series, upper_percentile)

    output = (series > lower_bound) * (series < upper_bound) * series + \
             (series <= lower_bound) * lower_bound + \
             (series >= upper_bound) * upper_bound
    auxiliary = _pd.DataFrame({'input': series, 'lower_bound': lower_bound, 'upper_bound': upper_bound,
                               'output': output})
    return output, auxiliary


def rank_and_standardize(series, *args, **kwargs):
    if 'Groupby_Item' in kwargs:
        groupby_item = kwargs['Groupby_Item']
        grouping = data_loader.Industry(kwargs['Universe']).map(groupby_item).reindex(series.index)
        rank = series.groupby(grouping).transform(_pd.Series.rank)
        mean = series.groupby(grouping).transform(_np.mean)
        std = series.groupby(grouping).transform(_np.std)
    else:
        rank = _pd.Series.rank(series)
        mean = _np.mean(series)
        std = _np.std(series)

    output = (rank - mean) / std
    auxiliary = _pd.DataFrame({'input': series, 'rank': rank, 'mean': mean, 'std': std,
                               'output': output})
    return output, auxiliary


def neutralize(series, *args, **kwargs):
    dummy_cols, dummy_dm = utils.create_dummy_for_neutralization(series, *args, **kwargs)
    y = series
    X = dummy_dm
    reg_result = _sm_api.OLS(y, X).fit()
    output = reg_result.resid
    auxiliary = _pd.DataFrame({'input': series, 'output': output})
    auxiliary = _pd.concat([auxiliary, dummy_dm], axis=1)
    return output, auxiliary


def allocate_risk_to_view():

    return


def vol_adjust():

    return





