from datetime import date

import Factory as Factory

import glob
import os.path
import os

#if __name__ == "__main__":

f = Factory.Factory()

service = f.create_collect_service()

service.execute()

#files = glob.glob("./db/*.csv")
#fund_names = [os.path.splitext(os.path.basename(file_name))[0] for file_name in files]"

name = "SEB Världenfond"

fund_names =[name]

l = f.create_loader(fund_names)
funds = l.execute()

df = funds[name]

g = f.create_graph_display(funds[name])
g.execute()

 