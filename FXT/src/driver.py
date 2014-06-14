#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.mock_model import MockModel
from src.mock_broker import MockBroker

class Driver():
    """
    Driver takes care of selecting model, broker and regime
    """
    def __init__(self):
        self.broker = self.init_broker()
        self.model = self.init_model()

    def init_broker(self):
        return MockBroker()

    def init_model(self):
        return MockModel('EUR_USD')

    def start(self):
        self.model.trade(self.broker)
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
