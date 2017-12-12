import numpy as _np
import pandas as _pd
import statsmodels.api as _sm_api
import datamaster.data_loader as data_loader


def trim_percentile(series, *args, **kwargs):
    lower_percentile = 0.01 if 'lower_percentile' not in kwargs else kwargs['lower_percentile']
    upper_percentile = 0.99 if 'upper_percentile' not in kwargs else kwargs['upper_percentile']
    if 'Groupby_Item' in kwargs:
        grouping = data_loader.Industry(kwargs['Universe']).map.reindex(series.index)
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
        grouping = data_loader.Industry(kwargs['Universe']).map.reindex(series.index)
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


def neutralize(df, *args, **kwargs):

    dummy = _create_dummy_for_neutralization(df, *args, **kwargs)
    dummy_cols = dummy['dummy_cols']
    df = dummy['df']

    y = df[kwargs['config']['column']]
    X = df[dummy_cols]

    reg_result = _sm_api.OLS(y, X).fit()

    df['weight'] = reg_result.resid
    df.drop(dummy_cols, axis=1, inplace=True)

    return df

def allocate_risk_to_view():

    return

def vol_adjust():

    return


"""
below are unit_test functions
"""


def _create_dummy_for_neutralization(df, *args, **kwargs):

    dummy_cols = []
    if 'beta' in kwargs['config']['neutralize_item']:
        for item in df[kwargs['config']['groupby_item']].unique():
            dummy_cols.append(item + 'beta_dummy')
            df[item + 'beta_dummy'] = df['beta'] * (df[kwargs['config']['groupby_item']] == item)
    if 'dollar' in kwargs['config']['neutralize_item']:
        for item in df[kwargs['config']['groupby_item']].unique():
            dummy_cols.append(item + 'dollar_dummy')
            df[item + 'dollar_dummy'] = 1.0 * (df[kwargs['config']['groupby_item']] == item)

    return {'dummy_cols': dummy_cols, 'df': df}



