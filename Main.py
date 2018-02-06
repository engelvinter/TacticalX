from datetime import datetime

from Utils import load_all, backtest, graph, Config, MONTHLY, YEARLY

selected = ['SEB Aktiesparfond', 'SEB Emerging Marketsfond', 'SEB Europa Småbolag', 
            'SEB Europafond', 'SEB Fastighetsfond', 'SEB Japanfond', 
            'SEB Latinamerikafond', 'SEB Läkemedelsfond', 'SEB Nordamerika Småbolag', 
            'SEB Nordamerikafond', 'SEB Nordenfond', 'SEB Schweizfond', 
            'SEB Sverigefond', 'SEB Teknologifond', 'SEB Trygg Placeringsfond', 
            'SEB Världenfond']

funds = load_all(selected)

def mom_rel():
    log_name = "mom_rel_{}".format(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
    
    c = Config()
    c.log_name = log_name
    c.name = "momentum rel"
    c.def_alloc = {'SEB Europafond' : 0.5, 'SEB Världenfond' : 0.5 }
    c.funds = funds
    c.algo = "mom_rel"
    c.freq = MONTHLY
    c.start = "2000-02-26"
    c.end = "2017-10-30"

    ts = backtest(c)
    return ts

ts = mom_rel()
graph("TAA", ts)


