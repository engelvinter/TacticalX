
import glob
import os.path
import os

import Factory as Factory

def collect():
    f = Factory.Factory()
    service = f.create_collect_service()
    service.execute()

def all_fund_names():
    files = glob.glob("./db/*.csv")
    fund_names = [os.path.splitext(os.path.basename(file_name))[0] for file_name in files]
    return fund_names

def load_all():
    f = Factory.Factory()
    l = f.create_loader(all_fund_names())
    funds = l.execute()
    return funds

def graph(fund):
    f = Factory.Factory()
    g = f.create_graph_display(fund)
    g.execute()