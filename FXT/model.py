#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from src.pricebuffer import PriceBuffer

class Model(metaclass=ABCMeta):
    def __init__(self, instrument, mode='all', pricebuffer_size=1000, **params):
        self.buffer = PriceBuffer(size=pricebuffer_size)
        self.instrument = tuple(instrument)
        self.mode = mode
        self.params = params

        self.trades = []

    @abstractmethod
    def train(self, tick_source_config, model_name):
        pass

    def open_position(self, broker, instrument, volume, order_type='market', expiry=None, **args):
        trade = broker.open(instrument, volume, order_type, expiry, **args)
        if trade:
            self.trades.append(trade)
        return trade

    def close_position(self, broker, trade):
        ret = broker.close(trade)
        if trade:
            self.trades.remove(trade)
        return ret

    @abstractmethod
    def trade(self, broker):
        pass

    def start(self, broker):
        if self.mode == 'trade':
            self.trade(broker)
        elif self.mode == 'train':
            self.train()
        elif self.mode == 'all':
            self.train()
            self.trade(broker)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
