
import glob
import os.path
import os

import pandas as pd

from Factory import Factory
from Print import Print

from SMA10 import SMA10
from Rebalance import Rebalance
from BuyAndHold import BuyAndHold
from RelativeMomentum import RelativeMomentum

MONTHLY     = "BMS"
QUARTERLY   = "BQS"
YEARLY      = "BAS"

def collect():
    f = Factory()
    service = f.create_collect_service()
    service.execute()

def all_fund_names():
    files = glob.glob("./db/*.csv")
    fund_names = [os.path.splitext(os.path.basename(file_name))[0] for file_name in files]
    return fund_names

def load_all(fund_names = None):
    f = Factory()
    if fund_names is None:
        fund_names = all_fund_names()
    l = f.create_loader(fund_names)
    funds = l.execute()
    return funds

def graph(title, *timeseries_list):
    colors = ["Blue", "Red", "Violet", "Green", "Magenta", "DeepPink", "DarkTurquoise", "DarkOrange"]
    colorNbr = 0
    f = Factory()
    g = f.create_graph_display(title)

    for timeseries in timeseries_list:
        g.add_timeseries(timeseries, colors[colorNbr % len(colors)])
        colorNbr += 1

    g.show()


class Config:
    funds       = None
    def_alloc   = None
    algo        = None
    freq        = YEARLY
    name        = ""
    start       = None
    end         = None

algorithms = {  "rebalance" :       lambda alloc : Rebalance(alloc),
                "sma10" :           lambda alloc : SMA10(alloc),
                "buy_and_hold" :    lambda alloc : BuyAndHold(alloc),
                "mom_rel" :         lambda alloc : RelativeMomentum(alloc, True) }


def backtest(config):
    f = Factory()
    logger = f.create_logger(config.log_name)

    algo = algorithms[config.algo](config.def_alloc)
    algo.set_logger(logger)

    bt = f.create_backtest(config.name, algo, config.freq, config.funds)
    bt.set_logger(logger)

    ts, result = bt.execute(config.start, config.end)
    pr = Print(result)
    pr.execute()

    
    return ts