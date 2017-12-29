import tushare as ts
import requests as _req
import json
import pandas as _pd
import datamaster.tushare.tushare_wrapper as ts_wrp

# df = ts.get_hist_data('600848',start='2015-01-05',end='2015-01-09')
# df_today = ts.get_today_all()
# df_report = ts.get_report_data(2017, 3)

#df0 = ts.get_balance_sheet('600518')

# specify a list of stocks, start, end --> get price data
df_price = ts_wrp.get_hists(symbols=['000001', '000002'], start='2017-09-26', end='2017-12-20')

# get cross sectional fundamental data
df_fundamental = ts_wrp.get_stock_basics('2017-09-26')

pass