#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class FXTTester():
    def __init__(self, model, test_data):
        self.test_data = model.convert_data(test_data)
        self.model = model
    
    def run_offline_test(self):
        for state_vector in self.model.get_next_state(test_data):
            print(self.model.decide(state_vector))
 
    def run_online_test(self):
        pass

if __name__ == '__main__':
    pass
  

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    