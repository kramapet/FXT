#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import bisect
import matplotlib.pyplot as pyplot

class Symbol():
    def __init__(self, symbol_name, values, dates):
        if len(values) != len(dates):
            raise(ValueError, "Values and dates must be the same size")
        
        self.dates = dates
        self.values = values
        self.symbol_name = symbol_name
        
        self.data_updated = True
        
    def _dt_to_idx(self, date, left=None):
        if date is None:
            return None

        i = bisect.bisect_left(self.dates, date)
        if left is None:
            if i != len(self.dates) and self.dates[i] == date:
                return i
            raise(ValueError)
        elif left == True:
            # Find leftmost item greater than or equal to date
            if i != len(self.dates):
                return i
            raise ValueError
        else:
            # Find rightmost value less than x
            if i:
                return i
            raise ValueError

    def _dt_slice_to_idx(self, arg):
        if isinstance(arg.start, datetime):
            start = self._dt_slice_to_idx(arg.start)
        else:
            start = arg.start
            
        if isinstance(arg.stop, datetime):
            stop = self._dt_slice_to_idx(arg.stop)
        else:
            stop = arg.stop
            
        return slice(start, stop, arg.step)

    def __len__(self):
        return len(self.dates)

    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return Symbol(self.symbol_name, self.values[self._dt_slice_to_idx(arg)],
                          self.dates[self._dt_slice_to_idx(arg)])
        else:
            if isinstance(arg, datetime.datetime):
                arg = self._dt_to_idx(arg)
            return (self.dates[arg], self.values[arg])
    
    def __iter__(self):
        return zip(self.dates, self.values)
    
    def __str__(self):
        output = "Symbol name: " + self.symbol_name + "\n"
        size = self.__len__()
        if size < 20:
            for i in range(size):
                output += "  " + str(self.dates[i]) + ": " + str(self.values[i]) + "\n"
        else:
            for i in range(5):
                output += "  " + str(self.dates[i]) + ": " + str(self.values[i]) + "\n"
            output += "    ...\n"
            for i in range(5, 0, -1):
                output += "  " + str(self.dates[i]) + ": " + str(self.values[i]) + "\n"
        output += "Number of elements: " + str(len(self.dates)) + "\n"
        return output

    def __delitem__(self, arg):
        self.data_updated = True
        if isinstance(arg, slice):
            arg = self._dt_slice_to_idx(arg)
        elif isinstance(arg, datetime.datetime):
            arg = self._dt_to_idx(arg)
        list.__delitem__(self.values, arg)
        list.__delitem__(self.dates, arg)

    def append(self, arg1, arg2=None):
        """Append arg1 to the arg1 and arg2 fields
           There are three append possibilities:
               Append another Symbol object
               Append two lists of arg1 and arg2
               Append single element with date
        """
        self.data_updated = True
        if arg2 is None:
            if isinstance(arg1, Symbol):
                list.extend(self.values, arg1.values)
                list.extend(self.dates, arg1.dates)
            else:
                raise(TypeError, "Only Symbol object, 2 lists of arg1/arg2 and single arg1/date can be appended.")    
        else:
            if isinstance(arg1, list) and isinstance(arg2, list):
                if len(arg1) != len(arg2):
                    raise(ValueError, "arg1 and arg2 must be the same size")
                self.values.extend(arg1)
                self.dates.extend(arg2)
            elif isinstance(arg2, datetime.datetime):
                self.values.append(arg1)
                self.dates.append(arg2)
            else:
                raise(TypeError, "Only Symbol object, 2 lists of arg1/arg2 and single arg1/date can be appended.")  
    
    def plot(self):
        pyplot.line = pyplot.plot(self.dates, self.values, label=self.symbol_name)
        pyplot.legend(loc='upper left')
        pyplot.show()

    

if __name__ == '__main__':
    symbol = Symbol("EURUSD", [(0,1), (1,2), (10,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10)], [datetime.datetime(2000, 1, (1+i)*2) for i in range (10)])

    print(symbol)
    
    # INDEXING TESTS
    #print(symbol[:])
    #print(symbol[1:3])
    #print(symbol[1:-1])
    #print(symbol[1])
    #print(symbol[datetime.datetime(2000, 1, 4)])
    #print(symbol[datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0):])
    #print(symbol[:datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0)])
    #print(symbol[datetime.datetime(2000, 1, 5, hour=23, minute=59, second=59):datetime.datetime(2000, 1, 10, hour=0, minute=0, second=1)])
    
    # DELETE TESTS
    #symbol.__delitem__(datetime.datetime(2000, 1, 4))
    #symbol.__delitem__(2)
    #symbol.__delitem__(-1)
    #symbol.__delitem__(datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0)) # should fail
    #symbol.__delitem__(slice(1, 8))
    #symbol.__delitem__(slice(datetime.datetime(2000, 1, 5, hour=23, minute=59, second=59), datetime.datetime(2000, 1, 10, hour=0, minute=0, second=1)))
    #sprint(symbol)

    # ITER TESTS
    #for i in symbol:
    #    print(i)

    # APPEND TESTS
    #symbol2 = Symbol("EURUSD", [(11,12), (12,13), (13,14)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)])
    #symbol.append(symbol2)
    #symbol.append([(11,12), (12,13), (13,14)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)])
    #symbol.append((11,12), datetime.datetime(2001, 1, 4))
    #symbol.append([(11,12), (12,13)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)]) # should fail
    
    #print(symbol)
    
    #symbol.plot()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    