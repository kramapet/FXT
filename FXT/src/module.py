#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Module(metaclass=ABCMeta):
    def __init__(self, train_data, params=None):
        self.train_data = train_data
        self.params = params
        self.model = None
    
    @abstractmethod
    def convert_data(self, data):
        """ Convert input data from values/dates to needed format
            
            Arguments:
                data data is a tupple of values/dates
            Returns:
                input data in appropriate format for implemented module
        """
        pass
    
    @abstractmethod
    def get_next_state(self, data):
        """ yields steps through input data 
        
            Arguments:
                data data allready processed by convert_data()
            Returns:
                state vector of actual state
        """
        pass
    
    @abstractmethod
    def train(self):
        pass
    
    
    @abstractmethod
    def decide(self, state_vector):
        """ decide what to do with current state vector
        
            Arguments: 
                state_vector state_vector contains current state that should be input to the date
            Returns:
                whether to buy[1], sell[-1] or do nothing[0]
        """
        pass

    

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4   