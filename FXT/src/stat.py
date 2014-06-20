#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Stat():
    def __init__(self, init_account_balance):
        self.buffer = pd.DataFrame()
        self.trades = []
        self.initial_account_balance = init_account_balance

    def add_tick(self, tick):
        new_tick = pd.DataFrame([tick], columns=['datetime', 'buy', 'sell'])
        new_tick.set_index('datetime', inplace=True)
        self.buffer = self.buffer.append(new_tick)

    def add_trade(self, trade):
        self.trades.append(trade)

    def plot(self):
        print(self.buffer)
        self.buffer.plot()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
