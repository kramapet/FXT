#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class Trade():
    def __init__(self, instrument, volume, open_price, margin_rate, sl=None, tp=None, id=None):
        self.instrument = instrument
        self.volume = volume
        self.open_rate = open_price
        self.close_rate = "STILL OPEN"
        self.trade_value = volume # TODO - this should be converted to the base currency of the instrument
        self.margin_rate = margin_rate
        self.margin = abs(self.trade_value) * margin_rate

    def __str__(self):
        if self.volume < 0:
            side = "sell"
        else:
            side = "buy"
        ret = "TRADE: " + side + " " + self.instrument[0] + "/" + self.instrument[1] + "\n"
        ret += "\tvolume: " + str(abs(self.volume)) + "\n"
        ret += "\topen rate: " + str(self.open_rate) + "\n"
        ret += "\tclose rate: " + str(self.close_rate) + "\n"
        ret += "\ttrade value: " + str(self.trade_value) + "\n"
        ret += "\tmargin: " + str(self.margin) + "\n"
        ret += "\tmargin rate: " + str(self.margin_rate) + "\n"
        return ret

    def close(self, close_price):
        self.close_rate = close_price

    def get_profit(self):
        return (self.close_rate - self.open_rate) * self.volume

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
