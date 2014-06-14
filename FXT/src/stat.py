#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Stat():
    def __init__(self):
        self.buffer = pd.DataFrame()

    def add_tick(self, tick):
        new_tick = pd.DataFrame([tick], columns=['datetime', 'buy', 'sell'])
        new_tick.set_index('datetime', inplace=True)

    def add_action(self, action):
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
