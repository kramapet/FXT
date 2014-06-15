#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.mock_model import MockModel
from src.mock_broker import MockBroker
from src.test_broker import TestBrokerLocal

class Driver():
    """
    Driver takes care of selecting model, broker and regime
    """
    def __init__(self):
        self.broker = self.init_broker()
        self.model = self.init_model()

    def init_broker(self):
        return TestBrokerLocal(account_balance=1000, start_date=datetime(2014, 4, 1), end_date=datetime.now())

    def init_model(self):
        return MockModel('EUR_USD')

    def start(self):
        self.model.trade(self.broker)
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
