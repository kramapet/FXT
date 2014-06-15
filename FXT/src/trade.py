#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class Trade():
    def __init__(self, instrument, volume, price,  id=None):
        self.instrument = instrument
        self.volume = volume
        self.price = price

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
