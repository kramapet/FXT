#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def train(self, train_data):
        pass

    @abstractmethod
    def trade(self, broker):
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
