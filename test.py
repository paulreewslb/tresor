from factor.factor import Factor
import matplotlib.pyplot as plt

if __name__ == '__main__':
    f = Factor(factor_name='P_212', start='2016-1-1', end='2017-12-10')
    f.update({'Universe': 'SP500_Consumer Discretionary_Apparel Retail'})
    #f.update({'Universe': 'SP500_Financials_Consumer Finance'})
    pnl, positions = f.backtest('BM')
    plt.plot(pnl.index, pnl)
    plt.show()