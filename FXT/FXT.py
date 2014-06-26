#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from src.driver import Driver

FORMAT = '%(asctime)s %(name)s: %(message)s'
logging.basicConfig(format=FORMAT)

driver = Driver()
driver.start()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4