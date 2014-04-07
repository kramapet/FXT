#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import bisect

class Symbol(list):
    def __init__(self, symbol_name, values, dates):
        if len(values) != len(dates):
            raise(ValueError, "Values and dates must be the same size")
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
        output += "Number of elements: " + str(len(self.dates)) + "\n"
        return output

    def __delitem__(self, arg):
        if isinstance(arg, int):
            list.__delitem__(self, arg)
            list.__delitem__(self.dates, arg)
        elif isinstance(arg, datetime.datetime):
            index = self._dt_to_idx(arg)
            list.__delitem__(self, index)
            list.__delitem__(self.dates, index)
    
    def __iter__(self):
        for element in zip(self.dates, list.__getitem__(self, slice(None, None))):
            yield element

    def append(self, values, dates=None):
        """Append values to the values and dates fields
           There are three append possibilities:
               Append another Symbol object
               Append two lists of values and dates
               Append single element with date
        """
        if dates is None:
            if isinstance(values, Symbol):
                list.extend(self, list(zip(*list(values)))[1]) #blah!
                list.extend(self.dates, values.dates)
            else:
                raise(TypeError, "Only Symbol object, 2 lists of values/dates and single values/date can be appended.")    
        else:
            if isinstance(values, list) and isinstance(dates, list):
                if len(values) != len(dates):
                    raise(ValueError, "values and dates must be the same size")
                list.extend(self, values)
                list.extend(self.dates, dates)
            elif isinstance(dates, datetime.datetime):
                list.append(self, values)
                list.append(self.dates, dates)
            else:
                raise(TypeError, "Only Symbol object, 2 lists of values/dates and single values/date can be appended.")  
    
    def plot(self):
        pass
    
    def save(self, path):
        if self.data_updated:
            # save to disk
            pass
    
    def load(self, path):
        pass


if __name__ == '__main__':
    symbol = Symbol("EURUSD", [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10)], [datetime.datetime(2000, 1, (1+i)*2) for i in range (10)])

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
    #symbol.__delitem__(datetime.datetime(2000, 1, 4, hour=20, minute=30, second=0))
    #print(symbol)

    # ITER TESTS
    #for i in symbol:
    #    print(i)

    # APPEND TESTS
    symbol2 = Symbol("EURUSD", [(11,12), (12,13), (13,14)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)])
    #symbol.append(symbol2)
    #symbol.append([(11,12), (12,13), (13,14)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)])
    #symbol.append((11,12), datetime.datetime(2001, 1, 4))
    #symbol.append([(11,12), (12,13)], [datetime.datetime(2001, 1, (1+i)*2) for i in range (3)])
    
    print(symbol)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    