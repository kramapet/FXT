#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Stat():
    def __init__(self, balance):
        self.buffer = []
        self.trades = []
        self.initial_account_balance = balance

    def add_tick(self, tick):
        self.buffer.append(tick)

    def add_trade(self, trade):
        self.trades.append(trade)

    def plot(self):
        print(self.buffer)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
