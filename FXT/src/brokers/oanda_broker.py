#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from collections import namedtuple

import src.thirdparty.oandapy.oandapy as oandapy
from src.stat import Stat
from src.trade import Trade


Tick = namedtuple("Tick", "datetime buy sell")

class OandaBroker():
    def __init__(self, enviroment):
        self.oanda = oandapy.API(environment=enviroment)
        
    def get_tick_data(self, instrument):
        while(1):
            response = self.oanda.get_prices(instruments=instrument[0] + "_" + instrument[1])
            t = response.get("prices")[0]        
            yield Tick(datetime.strptime(t['time'], '%Y-%m-%dT%H:%M:%S.%fZ'), t['ask'], t['bid'])

    def open(self, instrument, volume):
        # register trade

        return Trade(instrument, volume)

    def close(self, trade):
        pass

    def convert_currency(self, instrument, base_volume, rate=None):
        if rate:
            return base_volume * rate
        else:
            tick = self.get_tick_data(instrument)

            if base_volume > 0: # buy
                return tick[1] * base_volume
            else: # sell
                return tick[2] * abs(base_volume)

    def get_account_info(self):
        self.margin_rate = 0.05
        self.account_currency = 'EUR'

    def get_account_state(self):
        self.wallet = 1000
        self.trades = self.get_active_trades()

    def get_active_trades(self):
        return []

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4