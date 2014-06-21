#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from src.mock_broker import MockBroker
from src.test_broker import TestBrokerLocal

class Driver():
    """
    Driver takes care of selecting model, broker and regime
    """
    def __init__(self):
        self.config = self.read_config()

        self.broker = self.init_module('test_broker')
        self.model = self.init_module('model')

    def read_config(self):
        with open('config.json', 'r') as config:
            config = json.load(config)
        return config

    def init_module(self, module):
        import_string = "from " + self.config[module]['import'] + \
                        " import " + self.config[module]['class']
        params = ""
        for param_name in self.config[module]['params']:
            params += param_name + "=" + str(self.config[module]['params'][param_name]) + ", "

        exec(import_string)
        return eval(self.config[module]['class'] + "(" + params[:-2] + ")")

    def start(self):
        self.model.trade(self.broker)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
