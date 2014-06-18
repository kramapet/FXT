#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from src.model import Model

class MockModel(Model):
    """
    Model class
    """
    def train(self, instrument, train_data):
        pass

    def get_volume_for_price(self, broker, price, instrument_rate):
        """
        Get trade volume for given amount of money (broker.account_currency)
        equation used:
            profit = (Closing Rate - Opening Rate) * (Closing {quote}/{home currency}) * Units
        """
        conversion_rate = broker.get_tick_data((instrument[1], broker.account_currency))
        volume = price / (instrument_rate * conversion_rate)
        return volume

    def trade(self, broker):
        for tick in broker.get_tick_data(self.instrument):
            self.buffer.append(tick)

            # create pandas dataframe and resample data to 5s - example :-)
            df = pd.DataFrame(list(self.buffer), columns=['datetime', 'buy', 'sell'])
            df.set_index('datetime', inplace=True)
            resampled = df.resample('1Min', how={'buy':'ohlc', 'sell':'ohlc'})
            print(resampled)

            ## should we cose some trade?
            #for trade in trades:
            #   self.close_position(broker, trade)

            ## should we open some new trade?
            # do the magic and return 0/vlume/-volume
            # volume = xxx
            # self.open_position(broker, self.instrument, volume)



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
