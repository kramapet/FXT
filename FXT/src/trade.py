#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class Trade():
    def __init__(self, instrument, volume, open_price, margin_rate, sl=None, tp=None, id=None):
        self.instrument = instrument
        self.volume = volume
        self.open_price = open_price
        self.close_price = "STILL OPEN"
        self.trade_value = open_price * volume
        self.margin_rate = margin_rate
        self.margin = self.trade_value * margin_rate

    def __str__(self):
        if self.volume < 0:
            side = "sell"
        else:
            side = "buy"
        ret = "TRADE: " + side + " " + self.instrument[0] + "/" + self.instrument[1] + "\n"
        ret += "\tvolume: " + abs(self.volume) + "\n"
        ret += "\topen price: " + self.open_price + "\n"
        ret += "\tclose price: " + self.open_price + "\n"
        ret += "\topen price: " + self.open_price + "\n"
        ret += "\ttrade valu: " + self.trade_value + "\n"
        ret += "\tmargin: " + self.margin + "\n"
        ret += "\tmargin rate: " + self.margin_rate + "\n"
        return ret

    def close(self, close_price):
        self.close_price = close_price

    def get_profit(self):
        return (self.close_price - self.open_price) * self.volume

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
