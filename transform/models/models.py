import numpy as _np
import pandas as _pd
import scipy.stats as _st
import statsmodels.api as _sm_api


def trim_percentile(df, *args, **kwargs):

    if 'groupby_item' in kwargs['config']:
        df['lower_bound'] = df[[kwargs['config']['column']] + [kwargs['config']['groupby_item']]].\
            groupby(kwargs['config']['groupby_item']).\
            transform(lambda x:_np.percentile(x, 100 * kwargs['config']['lower_percentile']))
        df['upper_bound'] = df[[kwargs['config']['column']] + [kwargs['config']['groupby_item']]].\
            groupby(kwargs['config']['groupby_item']).\
            transform(lambda x:_np.percentile(x, 100 * kwargs['config']['upper_percentile']))
    else:
        df['lower_bound'] = _np.percentile(df[kwargs['config']['column']], kwargs['config']['lower_percentile'])
        df['upper_bound'] = _np.percentile(df[kwargs['config']['column']], kwargs['config']['upper_percentile'])

    df.loc[:,kwargs['config']['column']] = list(map(lambda origin, lower, upper: lower if origin < lower
                                                    else upper if origin > upper else origin,
                                                    df[kwargs['config']['column']], df['lower_bound'], df['upper_bound']))
    df.drop(['lower_bound', 'upper_bound'], axis=1, inplace=True)

    return df


def rank_and_standardize(df, *args, **kwargs):

    if 'groupby_item' in kwargs['config']:
        df['rank'] = df[[kwargs['config']['column']] + [kwargs['config']['groupby_item']]].\
            groupby(kwargs['config']['groupby_item']).transform(_st.rankdata)
        df['mean'] = df[['rank'] + [kwargs['config']['groupby_item']]].\
            groupby(kwargs['config']['groupby_item']).transform(_np.mean)
        df['std'] = df[['rank'] + [kwargs['config']['groupby_item']]].\
            groupby(kwargs['config']['groupby_item']).transform(_np.std)

    else:
        df['rank'] = _st.rankdata(df[kwargs['config']['column']])
        df['mean'] = _np.mean(df['rank'])
        df['std'] = _np.mean(df['std'])

    df['rank_std'] = (df['rank'] - df['mean']) / df['std']
    df.drop(['mean', 'std'], axis=1, inplace=True)

    return df


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



