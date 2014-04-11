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
        
    def __del__(self):
        self._store_internal_database()
        
    def _load_internal_database(self):
        """Load internal database containing all information abou allready learned data.
        """ 
        try:
            with open(self.DATABASE_DIR + "database.pkl", 'rb') as f:
                self.database = pickle.load(f)
        except:
            print("file: " + self.DATABASE_DIR + "database.pkl not found")

    def _load_symbol_data(self, symbol_name):
        """Load selected symbol from the pickle file.
        """ 
        try:
            with gzip.open(self.database[symbol_name]['pickle'], 'rb') as f:
                self.data[symbol_name] = pickle.load(f)
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
            if self.data[symbol_name].data_updated:
                print("Storing symbol", symbol_name, "to the database")
                self.data[symbol_name].data_updated = False
                with gzip.open(self.database[symbol_name]['pickle'], "wb") as f:
                    pickle.dump(self.data[symbol_name], f)
                    
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

    def _create_new_symbol(self, filename, symbol, starting_date):
        """Add newly read data to the database and create new symbol
        
        Args:
            filename: name of the source zip file
            symbol: name of the symbol
            starting_date: date extracted from the source zip file
        """ 
        values, dates = self._read_zip_file(filename)
        
        #update database
        self.database.setdefault(symbol, {})
        self.database[symbol]['pickle'] = self.DATABASE_DIR + symbol + ".pklz";
        self.database[symbol]['files'] = [filename];
        self.database[symbol]['first_date'] = dates[1];
        self.database[symbol]['last_date'] = dates[-1];
        
        # create symbol
        self.data[symbol] = Symbol(symbol, values, dates)
        
            
    def _add_to_existing_symbol(self, filename, symbol, starting_date):
        """Add newly read data to the database of allready existing symbol
        
        Args:
            filename: name of the source zip file
            symbol: name of the symbol
            starting_date: date extracted from the source zip file
        """ 
        
        if filename not in self.database[symbol]['files']:
            if starting_date > self.database[symbol]['last_date']:
                values, dates = self._read_zip_file(filename)
                
                # update database
                self.database[symbol]['files'].append(filename)
                self.database[symbol]['last_date'] = dates[-1]
                
                # append to the database
                self.data[symbol].append(values, dates)

            else:
                # TODO what if adding to the middle of the existing data?
                pass
    
    def update_internal_database(self):
        """Scan folder containing TrueFX data and update database if necessary
        """ 
        for filename in sorted(os.listdir("TFX_data")):
            if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                symbol, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
                symbol = symbol.upper()              
                starting_date = datetime.datetime(int(year), int(month), 1)
                if symbol in self.database:
                    self._add_to_existing_symbol(filename, symbol, starting_date)
                else:
                    self._create_new_symbol(filename, symbol, starting_date)

    def get_available_data_ranges(self, symbol=None):
        """Returns available data ranges for selected symbol (if the symbol is specified)
        Or all data ranges for all symbols in the database
        
        Args:
            symbol: selected symbol name (optional)
        Returns:
            list of data ranges for selected or for all symbols in the database
        """
        if symbol:
            if symbol in self.database:
                return (symbol, (self.database[symbol]['first_date'], self.database[symbol]['last_date']))
        else:
            if self.database:
                return [[sym, (self.database[sym]['first_date'], self.database[sym]['last_date'])] for sym in self.database]
        return None
        
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
        Returns:
            Symbol object of data or None when no data found
        """
        if symbol in self.database:
            if symbol not in self.data:
                self._load_symbol_data(symbol)
            return self.data[symbol][sl]
        else:
            return None

if __name__ == '__main__':
    #server = SimpleXMLRPCServer(("localhost", 8000))
    #server.register_instance(FXTDatastore())
    #server.serve_forever()
    #print("server started")
    dstore = FXTDatastore()
  

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    