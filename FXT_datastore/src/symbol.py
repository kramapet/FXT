#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import bisect

class Symbol(list):
    def __init__(self, symbol_name, values, dates):
        list.__init__(self, values)
        self.dates = dates
        self.symbol_name = symbol_name
        
        self.data_updated = False
        
    def _dt_to_idx(self, date, left=None):
        if date is None:
            return None
        if left is None:
            i = bisect.bisect_left(self.dates, date)
            if i != len(self.dates) and self.dates[i] == date:
                return i
            raise(ValueError)
        elif left == True:
            # Find leftmost item greater than or equal to date
            i = bisect.bisect_left(self.dates, date)
            if i != len(self.dates):
                return i
            raise ValueError
        else:
            # Find rightmost value less than x
            i = bisect.bisect_left(self.dates, date)
            if i:
                return i
            raise ValueError

    def __getitem__(self, arg):
        if isinstance(arg, slice):
            if ((isinstance(arg.start, int) or (arg.start == None)) and (isinstance(arg.stop, int) or (arg.stop == None))):
                return Symbol(self.symbol_name, list.__getitem__(self, arg), list.__getitem__(self.dates, arg))
            elif ((isinstance(arg.start, datetime.datetime) or (arg.start == None)) and (isinstance(arg.stop, datetime.datetime) or (arg.stop == None))):
                start = self._dt_to_idx(arg.start, left=True)
                stop = self._dt_to_idx(arg.stop, left=False)
                s = slice(start, stop)
                return Symbol(self.symbol_name, list.__getitem__(self, s), list.__getitem__(self.dates, s))
            else:
                raise(TypeError, "Invalid argument type.")  
        elif isinstance(arg, datetime.datetime):
            index = self._dt_to_idx(arg)
            return list.__getitem__(self, index)
        elif isinstance(arg, int):
            if arg < 0:
                arg += len(self)
            if arg >= len(self):
                raise(IndexError, "index out of range {}".format(arg))
            return (self.dates[arg], list.__getitem__(self, arg))
        else:
            raise(TypeError, "Invalid argument type.")  
    
    def __str__(self):
        output = "Symbol name: " + self.symbol_name + "\n"
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
        if self.data_updated:
            # save to disk
            pass
    
    def load(self, path):
        pass


if __name__ == '__main__':
    symbol = Symbol("EURUSD", [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10)], [datetime.datetime(2000, 1, (1+i)*2) for i in range (10)])
    print(symbol[:])
    #print(symbol[1:3])
    #print(symbol[1:-1])
    #print(symbol[1])
    #print(symbol[datetime.datetime(2000, 1, 4)])
    #print(symbol[datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0):])
    #print(symbol[:datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0)])
    print(symbol[datetime.datetime(2000, 1, 5, hour=23, minute=59, second=59):datetime.datetime(2000, 1, 10, hour=0, minute=0, second=1)])
    
    #symbol._dt_to_idx(datetime.date(2000, 1, 3, 12))
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    