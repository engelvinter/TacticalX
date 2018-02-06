from datetime import date

import os

from SebDownload import SebDownload
from SebExtract import SebExtract
from SebStore import SebStore
from SebLoad import SebLoad
from SebCollect import SebCollect
from SebGraphDisplay import SebGraphDisplay
from CollectService import CollectService
from SebFundOperations import SebFundOperations

from Backtest import Backtest

import logging

class Factory:
    def __init__(self):
        self._db_path = os.path.join(".", "db")
        self._graph_path = os.path.join(".", "graph")
        self._fund_min_days = 360

    def create_downloader(self, date):
        return SebDownload("https://seb.se/pow/fmk/2100", date)
    
    def create_extractor(self, content, fund_callback):
        return SebExtract(content, fund_callback)

    def create_storer(self, funds):
        return SebStore(self._db_path, funds)

    def create_collector(self, funds):
        return SebCollect(funds, self)

    def create_collect_service(self):
        first_date = date(1999, 2, 25)
        return CollectService(first_date, self._db_path, self)

    def create_loader(self, fund_names):
        return SebLoad(self._db_path, fund_names, self._fund_min_days)

    def create_graph_display(self, name):
        return SebGraphDisplay(name, self._graph_path)

    def create_fund_operations(self):
        return SebFundOperations()

    def create_logger(self, name):
        f = logging.FileHandler(name + ".txt", mode='w')
        l = logging.getLogger(name)
        l.setLevel(logging.INFO)
        l.addHandler(f)        
        return l

    def create_backtest(self, name, algo, freq, funds):
        bt = Backtest(name, algo, freq, funds)
        return bt
