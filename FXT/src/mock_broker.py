#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.stat import Stat

class MockBroker():
    def __init__(self):
        self.wallet = 1000;
        self.stat = Stat()

        self.trades = []

    def get_tick_data(self, instrument):
        while True:
            tick = (datetime.now(), 2, 1)
            self.stat.add_tick(tick)
            yield tick

    def open(self, instrument, volume):
        # register trade

        return Trade(instrument, volume)

    def close(self, trade):
        pass

    def get_account_state(self):
        pass

    def get_active_trades(self, instrument):
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
