#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from src.model import Model
from src.pricebuffer import PriceBuffer

class MockModel(Model):
    """
    Model class
    """
    def __init__(self, instrument):
        self.buffer = PriceBuffer(size=1000)

        self.instrument = instrument
        self.trades = []

    def train(self, symbol, train_data):
        pass

    def trade(self, broker):
        for tick in broker.get_tick_data(self.instrument):
            self.buffer.append(tick)

            # create pandas dataframe and resample data to 5s - example :-)
            df = pd.DataFrame(list(self.buffer), columns=['datetime', 'buy', 'sell'])
            df.set_index('datetime', inplace=True)
            resampled = df.resample('5s', how={'buy':'ohlc', 'sell':'ohlc'})
            print(resampled)

            # do the magic and return 0/vlume/-volume
            ret = 0

            if ret == 1:
                broker.buy(self.instrument, 1)
            elif ret == -1:
                broker.sell(self.instrument, 1)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
