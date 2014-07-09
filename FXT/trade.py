#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from FXT.stat import Stat

class Trade():
    def __init__(self, instrument, volume, open_price, open_datetime, id=None, **args):
        self.id = id
        self.instrument = instrument
        self.volume = volume
        self.open_rate = open_price
        self.open_datetime = open_datetime
        self.close_rate = "STILL OPEN"
        self.close_datetime = "STILL OPEN"
        self.profit = "STILL OPEN"
        self.args = args

    def __str__(self):
        if self.volume < 0:
            side = "sell"
        else:
            side = "buy"
        ret = "TRADE: " + side + " " + self.instrument[0] + "/" + self.instrument[1] + "\n"
        ret += "\tID: " + str(self.id) + "\n"
        ret += "\tvolume: " + str(abs(self.volume)) + "\n"
        ret += "\topen rate: " + str(self.open_rate) + "\n"
        ret += "\topen datetime: " + str(self.open_datetime) + "\n"
        ret += "\tclose rate: " + str(self.close_rate) + "\n"
        ret += "\tclose datetime: " + str(self.close_datetime) + "\n"
        ret += "\tprofit: " + str(self.profit) + "\n"
        return ret

    def close(self, close_price, close_datetime):
        self.close_rate = close_price
        self.close_datetime = close_datetime

    def set_profit(self, profit):
        self.profit = profit

    def get_profit(self):
        return (self.close_rate - self.open_rate) * self.volume

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
