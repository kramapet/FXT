#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: how about splitting the database file of each symbol per month? This is not very efficient..

import os
import re
import zipfile, io, csv
import datetime
import pickle, gzip
import datetime

from xmlrpc.server import SimpleXMLRPCServer

from src.symbol import Symbol

class FXTDatastore():
    TRUEFX_DIR = "TFX_data/"
    DATABASE_DIR = "db/"
    
    def __init__(self):
        self.data = {}
        self.database = {}
        
        self._load_internal_database()
        self.update_internal_database()
        self._store_internal_database()
        
    def _load_internal_database(self):
        """Load internal database containing all information abou allready learned data.
        """ 
        try:
            with open(self.DATABASE_DIR + "database.pkl", 'rb') as f:
                self.database = pickle.load(f)
        except:
            print("file: " + self.DATABASE_DIR + "database.pkl not found")

    def _load_symbol_data(self, symbol_name, year, month):
        """Load selected symbol from the pickle file.
        """ 
        try:
            with gzip.open(self.database[symbol_name][year][month]['pickle'], 'rb') as f:
                elf.data.setdefault(symbol, {}).setdefault(year, {}).setdefault(month, pickle.load(f))
        except:
            print("file: " + self.database[symbol_name]['pickle'] + " not found")
            
    def _store_internal_database(self):
        """Store internal database and changed symbols to the pickle files
        """ 
        # store database
        with open(self.DATABASE_DIR + "database.pkl", 'wb') as f:
            print("Storing database...")
            pickle.dump(self.database, f)

        # store data
        for symbol_name in self.data:
            for year in self.data[symbol_name]:
                for month in self.data[symbol_name][year]:
                    if self.data[symbol_name][year][month].data_updated:
                        print("Storing symbol", symbol_name, "year:", year , ", month:", month, "to the database")
                        self.data[symbol_name][year][month].data_updated = False
                        with gzip.open(self.database[symbol_name][year][month]['pickle'], "wb") as f:
                            pickle.dump(self.data[symbol_name][year][month], f)
                        print("done")
        print("finished")
                        
    def _read_zip_file(self, filename):
        """Read source zip file and generate values/dates
        
        Args:
            filename: name of the source zip file
        Returns:
            two lists containing values and dates from the zip file
        """ 
        values = []
        dates = []

        with zipfile.ZipFile(self.TRUEFX_DIR + filename) as zip_file:
            print("Opening file", self.TRUEFX_DIR + filename)
            csv_file = io.TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
            csv_reader = csv.reader(csv_file, delimiter=',')
            print("Adding data...")
            for i, row in enumerate(csv_reader):
                values.append((row[2], row[3]))
                dates.append(datetime.datetime.strptime(row[1], '%Y%m%d %H:%M:%S.%f'))
            print("Done adding data...")
        return values, dates;

    def _add_new_symbol(self, filename, symbol, year, month):
        """Add newly read data to the database and create new symbol
        
        Args:
            filename: name of the source zip file
            symbol: name of the symbol
            year: 
        """ 
        values, dates = self._read_zip_file(filename)
        
        #update database
        db_filename = self.DATABASE_DIR + symbol + "_" + year + "_" + month + ".pklz";
        self.database.setdefault(symbol, {}).setdefault(year, {}).setdefault(month, {})
        self.database[symbol][year][month]['pickle'] = db_filename
        self.database[symbol][year][month]['files'] = [filename];
        self.database[symbol][year][month]['first_date'] = dates[1];
        self.database[symbol][year][month]['last_date'] = dates[-1];
        
        # create symbol
        self.data.setdefault(symbol, {}).setdefault(year, {}).setdefault(month, Symbol(symbol, values, dates))

    def update_internal_database(self):
        """Scan folder containing TrueFX data and update database if necessary
        """ 
        for filename in sorted(os.listdir("TFX_data")):
            if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                symbol, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
                symbol = symbol.upper()              
                starting_date = datetime.datetime(int(year), int(month), 1)
                print("found file:", filename, ", symbol:", symbol, ", year:", year, ", month:", month)
                print(self.database)
                if symbol in self.database and year in self.database[symbol] and month in self.database[symbol][year]:
                    print("Allready in database")                            
                else:
                    self._add_new_symbol(filename, symbol, year, month)
                    

    def get_available_data_ranges(self, symbol=None):
        """Returns available data ranges for selected symbol (if the symbol is specified)
        Or all data ranges for all symbols in the database
        
        Args:
            symbol: selected symbol name (optional)
        Returns:
            list of data ranges for selected or for all symbols in the database
        """
        pass
        
    def get_available_symbols(self):
        """Returns all available symbol names
        
        Returns:
            List of all symbols
        """
        return self.database.keys()

    def get_data(self, symbol, sl):
        """Returns data of specified symbol and slice
        
        Args:
            symbol: selected symbol name
            sl: slice
        Returns:
            Symbol object of data or None when no data found
        """
        pass

if __name__ == '__main__':
    #server = SimpleXMLRPCServer(("localhost", 8000))
    #server.register_instance(FXTDatastore())
    #server.serve_forever()
    #print("server started")
    dstore = FXTDatastore()
  

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    