#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import rpyc
import pandas
import zipfile
import shutil
import datetime

class FXTDatastore(rpyc.Service):
    DB_FILE = os.getcwd() + "/data/DS_database.h5"
    TRUEFX_DIR = os.getcwd() + "/trueFX/"
    
    def __init__(self, conn=None):
        if conn:
            rpyc.Service.__init__(self, conn)
        else:
            self.DB_FILE = os.getcwd() + "/../data/DS_database.h5"
            self.TRUEFX_DIR = os.getcwd() + "/../trueFX/"
        self._load_internal_database()
        #self.update_internal_database()
    
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
    
    def _load_internal_database(self):
        """
            This method loads internal pandas database containing all collected data
            If the database doesn't exist, create new one and set indexes to symbol and timestamp.
        """
        print("Loading internal database...")
        try:
            self.database = pandas.read_hdf(self.DB_FILE, 'database')
            print("Database loaded...")
        except:
            self.database = pandas.DataFrame({'symbol': [], 'timestamp' : [], 'ask':[], 'bid':[]})
            self.database.set_index(['symbol', 'timestamp'], inplace=True)
            
            print("Database not found, new one created...")
        
    def _store_internal_database(self):
        self.database.to_hdf(self.DB_FILE, 'database', mode='w')
        
    def update_internal_database(self):
        """
        Scan trueFX folder and calls self._add_file_to_database() to update internal database
        """ 
        print("Updating internal database...")
        changed = False
        tfx_directory = self.TRUEFX_DIR
        for filename in os.listdir(tfx_directory):
            if filename.endswith(".zip") or filename.endswith(".ZIP"):
                if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                    changed = True
                    self._add_file_to_database(filename)
                    shutil.move(tfx_directory + filename, tfx_directory + "applied/" + filename)
        if changed:
            self._store_internal_database()
            print("Database updated...")
        else:
            print("Nothing to update")

    def _add_file_to_database(self, filename):
        """
        Update internal database if contents of the zip file was not yet added to database
        """
        print("Processing new file:", filename)
        
        # process filename
        symbol, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
        year = int(year); month = int(month)
        symbol = symbol[:3] + '/' + symbol[3:]
        
        # add to the database
    
        zip_filename = self.TRUEFX_DIR + filename
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            csv_file = zip_file.open(zip_file.namelist()[0])
            df = pandas.read_csv(csv_file, names=['symbol', 'timestamp', 'bid', 'ask'],
                                 converters={'date_time': lambda x: datetime.datetime.strptime(x, '%Y%m%d %H:%M:%S.%f')})
        
        # ugly ugly trick TODO!!!
        self.database.reset_index(inplace=True)
        self.database = self.database.append(df)
        self.database.drop_duplicates(take_last=True, inplace=True)
        self.database.set_index(['symbol', 'timestamp'], inplace=True)
        print("\tStored new data...")
        
    def exposed_get_data_ranges(self, symbol=None):
        #if symbol:
        #    try:
        #        df = self.datastore[self.datastore['symbol'] == symbol]
        #    except:
        #        pass
        #TODO return dictionary with start date- stop_date for each symbol
        result = {}
        symbols = list(self.database.index.levels[0])
        for symbol in symbols:
            result[symbol] = (self.database.ix[symbol].ix[0], self.database.ix[symbol].ix[-1])
        return result
        
        
    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"


if __name__ == '__main__':
    datastore = FXTDatastore()
    print(datastore.exposed_get_data_ranges())
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    