import numpy as _np
import pandas as _pd

import data_handler.data_analyzer as data_api

import quandl
import data_handler.good_morning as gm

quandl.ApiConfig.api_key = 'myyzV9yQuCz7LR_2k-43'

class Beta(object):

    def __init__(self, asset_list):

        self.asset_list = asset_list
        self.asset_ret = data_api.Share.get_change()

    def _get_asset_returns(self):

        ret_list = []
        for elem in self.asset_list:
            asset = data_api.Share.get_change()


class RealizedBeta(Beta):



