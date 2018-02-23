
import glob
import os.path
import os

import re

import pandas as pd

from datetime import datetime

from Factory import Factory
from Print import Print

from SMA10 import SMA10
from Rebalance import Rebalance
from BuyAndHold import BuyAndHold
from RelativeMomentum import RelativeMomentum

MONTHLY     = "BMS"
QUARTERLY   = "BQS"
YEARLY      = "BAS"

class Config:
    funds       = None
    def_alloc   = None
    algo        = None
    freq        = YEARLY
    name        = ""
    start       = None
    end         = None

_algorithms = {  
                "rebalance" :       lambda alloc : Rebalance(alloc),
                "sma10" :           lambda alloc : SMA10(alloc),
                "buy_and_hold" :    lambda alloc : BuyAndHold(alloc),
                "mom_rel" :         lambda alloc : RelativeMomentum(alloc)
              }

def collect():
    f = Factory()
    service = f.create_collect_service()
    service.execute()

def all_fund_names(regexp = ".*"):
    files = glob.glob("./db/*.csv")
    extract_base = lambda fullpath :  os.path.splitext(os.path.basename(fullpath))[0]
    all_fund_names = [extract_base(fullpath) for fullpath in files]
    fund_names = [name for name in all_fund_names if re.match(regexp, name)]
    return fund_names

def load_all(*fund_names):
    f = Factory()
    
    names_to_load = []
    if len(fund_names) is 0:
        names_to_load = all_fund_names()
    else:
        names_to_load = all_fund_names("|".join(fund_names))
        
    l = f.create_loader(names_to_load)
    funds = l.execute()
    return funds

def graph(title, *timeseries_list, dir_name = "temp", normalize = True):
    colors = ["Blue", "Red", "Violet", "Green", "Magenta", "DeepPink", "DarkTurquoise", "DarkOrange"]
    colorNbr = 0
    f = Factory()
    g = f.create_graph_display(title, dir_name)

    for timeseries in timeseries_list:
        ts = timeseries
        if normalize:
            ts = timeseries / timeseries[0]
        g.add_timeseries(ts, colors[colorNbr % len(colors)])
        colorNbr += 1

    return g

def backtest(config):
    dir_name = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

    f = Factory()    
    logger = f.create_logger(dir_name)

    algo = _algorithms[config.algo](config.def_alloc)
    algo.set_logger(logger)

    bt = f.create_backtest(config.name, algo, config.freq, config.funds)
    bt.set_logger(logger)

    ts, result = bt.execute(config.start, config.end)

    printer = f.create_printer(result, dir_name)
    printer.execute()

    g = graph(config.name, dir_name, ts)
    g.create_file()

    return ts