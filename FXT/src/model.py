#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from src.pricebuffer import PriceBuffer

class Model(metaclass=ABCMeta):
    def __init__(self, instrument, pricebuffer_size=1000):
        self.buffer = PriceBuffer(size=pricebuffer_size)

        self.instrument = instrument
        self.trades = []

    @abstractmethod
    def train(self, train_data):
        pass

    def open_position(self, broker, instrument, volume, **args):
        trade = broker.open(instrument, volume, args)
        self.trades.append(trade)

    def close_position(self, broker, trade):
        broker.close(trade)
        self.trades.remove(trade)

    @abstractmethod
    def trade(self, broker):
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
