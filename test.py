from factor.factor import Factor
import pandas as pd

if __name__ == '__main__':
    f = Factor(factor_name='P_212', start='2017-1-1', end='2017-12-10')
    f.update({'Universe': 'SP500_Consumer Discretionary_Apparel Retail'})
    f.views
    f.backtest('BM')