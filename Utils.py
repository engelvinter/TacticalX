
import glob
import os.path
import os

import pandas as pd

import Factory as Factory

def collect():
    f = Factory.Factory()
    service = f.create_collect_service()
    service.execute()

def all_fund_names():
    files = glob.glob("./db/*.csv")
    fund_names = [os.path.splitext(os.path.basename(file_name))[0] for file_name in files]
    return fund_names

def load_all(fund_names = None):
    f = Factory.Factory()
    if fund_names is None:
        fund_names = all_fund_names()
    l = f.create_loader(fund_names)
    funds = l.execute()
    return funds

def graph(timeseries):
    f = Factory.Factory()
    g = f.create_graph_display(timeseries)
    g.execute()

