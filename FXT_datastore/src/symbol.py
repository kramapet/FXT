#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class Symbol(list):
    def __init__(self, symbol_name, values, dates):
        list.__init__(self, values)
        self.dates = dates
        self.symbol_name = symbol_name
        
        self.data_updated = False
        
    def _dt_to_idx(self, date, larger=True):
        # TODO, find closest date from dates and return index
        # if larger is set to true searching for closest larger date, else for smaller
        print(min(self, key=lambda x: abs(date-x)))
        
    def __getitem__(self, date):
        if isinstance(date, slice):
            start = date.start
            end = date.stop
            if ((isinstance(start, int) or (start == None)) and (isinstance(end, int) or (end == None))):
                return Symbol(self.symbol_name, list.__getitem__(self, date), list.__getitem__(self.dates, date))
            elif ((isinstance(start, datetime.date) or (start == None)) and (isinstance(end, datetime.date) or (end == None))):
                #return [list.__getitem__(self, i) for i in range(start, end)]
                pass
            else:
                raise(TypeError, "Invalid argument type.")  
                
        elif isinstance(date, datetime.date):
            index = self.get_index(date)
            return list.__getitem__(self, index)
        elif isinstance(date, int):
            if date < 0:
                date += len(self)
            if date >= len(self):
                raise(IndexError, "index out of range {}".format(date))
            return list.__getitem__(self, date)
        else:
            raise(TypeError, "Invalid argument type.")  
    
    def __str__(self):
        output = "Symbol class name: " + self.symbol_name + "\n"
        size = list.__len__(self)
        if size < 20:
            for i in range(size):
                output += "  " + str(self.dates[i]) + ": " + str(list.__getitem__(self, i)) + "\n"
        else:
            for i in range(5):
                output += "  " + str(self.dates[i]) + ": " + str(list.__getitem__(self, i)) + "\n"
            output += "    ...\n"
            for i in range(5, 0, -1):
                output += "  " + str(self.dates[i]) + ": " + str(list.__getitem__(self, i)) + "\n"
        
        return output
        
    def __repr__(self):
        pass

    def append(self, data, dates=None):
        """Append data to the data and dates fields"""
        if dates is None:
            for entry in data:
                if isinstance(entry[1], list) or isinstance(entry[1], tuple):
                    # format: data = [(date, (ask, bid)), ... ]
                    list.append(entry[1])
                    self.dates.append(entry[0])
                else:
                    # format: data = [((ask, bid), date), ... ]
                    list.append(entry[1])
                    self.dates.append(entry[0])
                    
        else:
            # format: data = [(ask, bid), ...] , dates = (date, ...)
            list.append(data)
            self.dates.append(dates)

    def delete(self, start_date, stop_date):
        pass
    
    def save(self, path):
        pass
    
    def load(self, path):
        pass


if __name__ == '__main__':
    symbol = Symbol("EURUSD", [(0,1), (1,2), (2,3), (3,4), (4,5)], [datetime.date(2000, 1, (1+i)*2) for i in range (5)])
    print(symbol[1:2])
    #symbol._dt_to_idx(datetime.date(2000, 1, 3, 12))
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    