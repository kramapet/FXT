#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Stat():
    def __init__(self, init_account_balance):
        self.buffer = []
        self.trades = []
        self.initial_account_balance = init_account_balance

    def add_tick(self, tick):
        self.buffer.append(tick)

    def add_trade(self, trade):
        self.trades.append(trade)

    def plot(self):
        print(self.buffer)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
