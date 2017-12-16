import pandas as _pd
import datamaster.data_loader as data_loader
import numpy as np


def create_dummy_for_neutralization(series, *args, **kwargs):
    dummy_cols = []
    dummy_dm = _pd.DataFrame(index=series.index)
    if 'Groupby_Item' in kwargs:
        groupby_item = kwargs['Groupby_Item']
        grouping = data_loader.Industry(kwargs['Universe']).map(groupby_item).reindex(series.index)
    beta = np.random.rand(len(series))  # need to add code for beta and reindex by series.index
    if 'beta' in kwargs['Neutralize_Item']:
        if 'Groupby_Item' in kwargs:
            for item in grouping.unique():
                dummy_cols.append(item + '_beta_dummy')
                dummy_dm[item+'_beta_dummy'] = beta * (grouping == item)
        else:
            dummy_cols.append('beta_dummy')
            dummy_dm['beta_dummy'] = beta
    if 'dollar' in kwargs['Neutralize_Item']:
        if 'Groupby_Item' in kwargs:
            for item in grouping.unique():
                dummy_cols.append(item + '_dollar_dummy')
                dummy_dm[item+'_dollar_dummy'] = 1.0 * (grouping == item)
        else:
            dummy_cols.append('dollar_dummy')
            dummy_dm['dollar_dummy'] = 1

    return dummy_cols, dummy_dm