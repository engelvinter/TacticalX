from datetime import date

import SebDownload
import SebExtract
import SebStore
import SebLoad
import SebCollect
import SebGraphDisplay
import CollectService
import SebFundOperations

import logging

class Factory:
    def __init__(self):
        self._db_path = "./db"
        self._graph_path = "./graph"
        self._fund_min_days = 360

    def create_downloader(self, date):
        return SebDownload.SebDownload("https://seb.se/pow/fmk/2100", date)
    
    def create_extractor(self, content, fund_callback):
        return SebExtract.SebExtract(content, fund_callback)

    def create_storer(self, funds):
        return SebStore.SebStore(self._db_path, funds)

    def create_collector(self, funds):
        return SebCollect.SebCollect(funds, self)

    def create_collect_service(self):
        first_date = date(1999, 2, 25)
        return CollectService.CollectService(first_date, self._db_path, self)

    def create_loader(self, fund_names):
        return SebLoad.SebLoad(self._db_path, fund_names, self._fund_min_days)

    def create_graph_display(self, timeseries):
        return SebGraphDisplay.SebGraphDisplay(timeseries, self._graph_path)

    def create_fund_operations(self):
        return SebFundOperations.SebFundOperations()

    def create_transaction_logger(self):
        f = logging.FileHandler("transactions.txt")
        l = logging.getLogger("transaction")
        l.setLevel(logging.INFO)
        l.addHandler(f)

        return l
