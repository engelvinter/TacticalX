import pandas as pd

import os

class SebStore:
    def __init__(self, db_path, funds):
        self._funds = funds
        self._path = db_path

    def execute(self):
        for fund in self._funds:
            filename = "{0}/{1}.csv".format(self._path, fund)
            header = False if os.path.isfile(filename) else True
            with open(filename, 'a') as f:
                self._funds[fund].to_csv(f, header = header)