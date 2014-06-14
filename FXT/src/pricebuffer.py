#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

class PriceBuffer(deque):
    def __init__(self, size=1000):
        super(PriceBuffer, self).__init__(maxlen=size)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
