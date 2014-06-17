#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io, csv, zipfile
import re
from datetime import datetime

class LocalData():
    TFX_DIR = 'TFX_data/'
    
    def __init__(self):
        pass

    def _scan_tfx_directory(self):
        database = {}
        for filename in sorted(os.listdir("TFX_data")):
            if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                instrument, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
                instrument = instrument.upper()
                starting_date = datetime(int(year), int(month), 1)
                database.setdefault(instrument, {}).setdefault(starting_date, filename)
        return database

    def read_tfx_files(self, instrument, start_date, end_date):
        """
        Read the TFX
        """
        db = self._scan_tfx_directory()
        filenames = [db[instrument][k] for k in sorted(db[instrument]) if end_date > k >= start_date]

        for filename in filenames:
            with zipfile.ZipFile(self.TFX_DIR + filename) as zip_file:
                csv_file = io.TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
                csv_reader = csv.reader(csv_file, delimiter=',')
                for i, row in enumerate(csv_reader):
                    tick_datetime = datetime.strptime(row[1], '%Y%m%d %H:%M:%S.%f')
                    if start_date >= tick_datetime > end_date:
                        next
                    else:
                        yield (tick_datetime, float(row[2]), float(row[3]))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
