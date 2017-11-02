from datetime import date, datetime

import Factory as Factory

import Utils

import SebFixedAlloc

#if __name__ == "__main__":

#f = Factory.Factory()

#service = f.create_collect_service()
#service.execute()

#name = "Carnegie Corporate Bond"
#fund_names =[name]

#fund_names = ["SEB Världenfond", "SEB Forskning", "Turkietfonden", "SEB Europafond"]

#fund_names = ['SEB Östeuropafond', 'SEB Emerging Marketsfond', 'SEB Europafond', 'SEB Nordenfond', 'SEB Sverigefond', 'SEB Läkemedelsfond', 'SEB Japanfond', 'SEB Världenfond', 'SEB Fastighetsfond', 'SEB Latinamerikafond', 'SEB Aktiesparfond', 'SEB Nordamerikafond', 'SEB Teknologifond']

#l = f.create_loader(fund_names)
#funds = l.execute()

#print(interval(funds, start, end))

#g = f.create_graph_display(funds[name])
#g.execute()

start = datetime(1999, 3, 1)
end = datetime(2017, 10, 20)

funds = Utils.load_all()

fixed_alloc = { "SEB Världenfond" : 1.0 }

alloc = SebFixedAlloc.SebFixedAlloc(funds, fixed_alloc, start, end)
alloc.current_portfolio_value(10000)
alloc.execute()

