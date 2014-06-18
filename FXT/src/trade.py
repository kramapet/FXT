#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class Trade():
    def __init__(self, instrument, volume, open_price, margin_rate, id=None):
        self.instrument = instrument
        self.volume = volume
        self.price = open_price
        self.trade_value = open_price * volume
        self.margin = self.trade_value * margin_rate
        
    def get_profit(self, close_price):
        return (self.close_price - self.open_price) * self.volume
        
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
