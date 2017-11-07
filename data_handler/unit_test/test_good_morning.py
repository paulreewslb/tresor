import numpy as _np
import pandas as _pd

import data_handler.good_morning.good_morning as gm

kr = gm.FinancialsDownloader()
kr_fins = kr.download('AAPL')

print(kr_fins)