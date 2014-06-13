#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: how about splitting the database file of each symbol per month? This is not very efficient..

import os
import re
import zipfile, io, csv
import pickle, gzip
from datetime import datetime

from src.symbol import Symbol
from FXTDatastore import FXTDatastore

class FXT(object):
    def __init__(self):
        self.datastore = FXTDatastore()
        
        self.symbol = None
        self.train_set = None
        self.test_set = None
        
        self.data = None
        
    def start(self):
        pass
    
    def set_module(self, module):
        pass
    
    def set_train_set(self, dates=None, indices=None):
        self.train_set = {'dates':dates, 'indices':indices}
    
    def set_test_set(self, dates=None, indices=None):
        self.test_set = {'dates':dates, 'indices':indices}
    
    def set_symbol(self, symbol):
        self.symbol = symbol;

    def _get_data(self):
        """ load desired data from the data files to the memory
        self.set_train_set() and self.set_test_set() should be called before
        Args:
            None
        Return: 
            None
        """
        train_set_files = None
        test_set_files = None
        if self.symbol:
            if self.train_set:
                if self.train_set['dates']:
                    train_set_files = self.datastore.get_filenames_by_dates(self.symbol, self.train_set['dates'])
                else:
                    train_set_files = self.datastore.get_filenames_by_indices(self.symbol, self.train_set['indices'])
            
            if self.test_set:
                if self.test_set['dates']:
                    test_set_files = self.datastore.get_filenames_by_dates(self.symbol, self.test_set['dates'])
                else:
                    test_set_files = self.datastore.get_filenames_by_indices(self.symbol, self.test_set['indices'])
    
        # merge the two sets - remove duplicates
        all_files = list(set(train_set_files) | set(test_set_files))
        
        print("all_files:", all_files)

        #get all data
        self.data = self.datastore.read_files(all_files)


    def start(self):
        self._get_data()

if __name__ == '__main__':
    fxt = FXT()
    fxt.set_symbol('EURUSD')
    fxt.set_train_set(dates=(datetime(2014, 1, 1), datetime(2014, 3, 1)))
    fxt.set_test_set(dates=(datetime(2014, 3, 1), datetime(2014, 4, 1)))
    fxt.start()
    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    