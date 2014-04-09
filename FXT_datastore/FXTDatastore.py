#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import zipfile
import datetime
import pickle
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
        
    def _load_internal_database(self):
        """
            This method loads internal pandas database containing all collected data
            If the database doesn't exist, create new one and set indexes to symbol and timestamp.
        """
        try:
            with open(self.DATABASE_DIR + "database.pickle", 'r') as f:
                self.database = pickle.load(f)
        except:
            print("file: ", self.DATABASE_DIR, "database.pickle not found")
        
        for symbol_name in self.database:
            try:
                with open(self.database[symbol_name]['pickle'], 'r') as f:
                    self.data[symbol_name] = pickle.load(f)
            except:
                print("file: " + self.database[symbol_name]['pickle'] + " not found")
            
    def _store_internal_database(self):
        # store data
        for symbol_name in self.database:
            if self.data[symbol_name].data_updated:
                self.data[symbol_name] = False
                with open(self.database[symbol_name]['pickle'], "w") as f:
                    pickle.dump(self.data[symbol_name], f)
                    
        # store database
        with open(self.DATABASE_DIR + "database.pickle", 'w') as f:
            pickle.dump(self.database, f)


    def _read_zip_file(self, filename):
        values = []
        dates = []
        
        with zipfile.ZipFile(self.TRUEFX_DIR + filename, 'r') as zip_file:
            csv_file = zip_file.open(zip_file.namelist()[0])
            # TODO
        
        return values, dates;

    def _create_new_symbol(self, filename, symbol, starting_date):
        values, dates = self._read_zip_file(filename)
        
        #update database
        self.database[symbol]['pickle'] = symbol + ".pickle"
        self.database[symbol]['files'] = [filename]
        self.database[symbol]['first_date'] = dates[1]
        self.database[symbol]['last_date'] = dates[-1]
        
        # create symbol
        self.data[symbol] = Symbol(symbol, values, dates)
        
            
    def _add_to_existing_symbol(self, filename, symbol, starting_date):
        if filename not in self.database[symbol]['files']:
            if starting_date > last_date:
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
        """
        Scan trueFX folder and calls self._add_file_to_database() to update internal database
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
        pass
        
    def get_available_symbols(self):
        pass
        
    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(FXTDatastore())
    server.serve_forever()
    print("server started")
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    