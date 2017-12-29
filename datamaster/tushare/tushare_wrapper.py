from tushare import *


# this needs to be implemented as decorator in the future
def translate(df, func_name, *args, **kwargs):

    assert func_name in kwargs['config']

    if 'columns' in kwargs['config'][func_name]:
        df.columns = map(kwargs['config'][func_name]['columns'].get, df.columns)
    if 'indices' in kwargs['config'][func_name]:
        df.index = map(kwargs['config'][func_name]['indices'].get, df.index)

    return df

