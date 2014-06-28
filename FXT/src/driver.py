#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import importlib
import logging
from datetime import datetime

class Driver():
    """
    Driver takes care of selecting model, broker and regime
    """
    def __init__(self):
        self.config = self.read_config()

        self.broker = self.init_module(self.config['use']['broker'])
        self.model = self.init_module(self.config['use']['model'])

        logging.basicConfig(format=self.config['use']['log_format'], level=self.config['use']['log_level'])

    def read_config(self):
        with open('config.json', 'r') as config:
            config = json.load(config)
            return config

    def init_module(self, module_str):
        module_config = self.config[module_str]
        return self.init_module_config(module_config)

    @staticmethod
    def init_module_config(module_config):
        params = {k:v for k,v in module_config.items() if k not in ['import', 'class']}

        module = importlib.import_module(module_config['import'])
        return getattr(module, module_config['class'])(**params)

    def start(self):
        self.model.trade(self.broker)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
