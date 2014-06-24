#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import importlib
from datetime import datetime

class Driver():
    """
    Driver takes care of selecting model, broker and regime
    """
    def __init__(self):
        self.config = self.read_config()

        self.broker = self.init_module(self.config['use']['broker'])
        self.model = self.init_module(self.config['use']['model'])

    def read_config(self):
        with open('config.json', 'r') as config:
            config = json.load(config)
            return config

    def init_module(self, module_str):
        module = importlib.import_module(self.config[module_str]['import'])

        params = ""
        for param_name in self.config[module_str]['params']:
            params += param_name + "=" + str(self.config[module_str]['params'][param_name]) + ", "

        return eval("module." + self.config[module_str]['class'] +"(" + params[:-2] + ")")

    def start(self):
        self.model.trade(self.broker)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
