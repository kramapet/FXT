#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import zipfile, io, csv
from datetime import datetime
from collections import OrderedDict

class FXTDatastore():
    TRUEFX_DIR = "TFX_data/"
    DATABASE_DIR = "db/"
    
    def __init__(self):
        self.database = {}
        self.scan_db_directory()
        
    def _read_zip_file(self, filename):
        """Read source zip file/s and generate values/dates
        
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
            print("reading CSV data...")
            for i, row in enumerate(csv_reader):
                values.append((row[2], row[3]))
                dates.append(datetime.strptime(row[1], '%Y%m%d %H:%M:%S.%f'))
        return values, dates;

    def read_files(self, files):
        """ read each file of input files list create values/dates lists for
        each of these input files
        Args:
            files list of file names to be read
        Returns:
            dict of dates/values for each file read
        """
        ret = {}
        for filename in files:
            ret[filename] = self._read_zip_file(filename)
        return ret

    def scan_db_directory(self):
        """Scan folder containing TrueFX data and find all present TFX zip files
        """ 
        for filename in sorted(os.listdir("TFX_data")):
            if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                symbol, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
                symbol = symbol.upper()              
                starting_date = datetime(int(year), int(month), 1)
                self.database.setdefault(symbol, {}).setdefault(starting_date, filename)
    
    def get_filenames_by_dates(self, symbol, dates):
        start_date, end_date = dates
        return [self.database[symbol][k] for k in sorted(self.database[symbol]) if end_date > k >= start_date]

    
    def get_filenames_by_indices(self, symbol, indices):
        start_index, end_index = indices
        return [self.database[symbol][k] for k in OrderedDict(sorted(self.database[symbol].items()))][start_index, end_index]
        
        
    
if __name__ == '__main__':
    fxtd = FXTDatastore()
    print (fxtd.database)
  

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4    