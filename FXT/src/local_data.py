#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import re

class LocalData():
    def __init__(self):
        pass

    def _scan_tfx_directory(self):
        database = {}
        for filename in sorted(os.listdir("TFX_data")):
            if re.match(r'[A-Z]{6}-\d{4}-\d{2}.zip', filename):
                instrumnet, year, month = re.match(r'([A-Z]{6})-(\d{4})-(\d{2}).zip', filename).groups()
                instrumnet = instrumnet.upper()
                starting_date = datetime(int(year), int(month), 1)
                database.setdefault(instrumnet, {}).setdefault(starting_date, filename)
        return database

    def read_tfx_files(self, start_date, end_date, instrumnet):
        """
        Read the TFX
        """
        db = self._scan_tfx_directory()
        filenames = [db[instrumnet][k] for k in sorted(db[instrumnet]) if end > k >= start]

        for filename in filenames:
            with zipfile.ZipFile(self.TRUEFX_DIR + filename) as zip_file:
                csv_file = io.TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
                csv_reader = csv.reader(csv_file, delimiter=',')
                for i, row in enumerate(csv_reader):
                    tick_datetime = datetime.strptime(row[1], '%Y%m%d %H:%M:%S.%f')
                    if start_date >= tick_datetime > end_date:
                        next
                    else:
                        yield (tick_datetime, row[2], row[3])

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
