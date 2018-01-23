from datetime import date, datetime

import Factory as Factory

import Utils

import SebFundOperations

import Simulate

import BuyAndHold
import Rebalance
import SMA10
import RelativeMomentum

import Market

import Portfolio

import Evaluate

import Print

def test_algo(funds, algo, logger, freq):
    start = datetime(2000, 2, 26)
    end = datetime(2017, 10, 30)
    ops = SebFundOperations.SebFundOperations()
  
    s = Simulate.Simulate(start, end)
    s.setup_reallocations(algo, freq)

    p = Portfolio.Portfolio(10000)

    m = Market.Market(funds, p, logger)

    ts = s.execute(m)
    ts.name = algo.name

    e = Evaluate.Evaluate(ts)
    result = e.execute()

    pr = Print.Print(result)
    pr.execute()

    return ts

def setup_buy_and_hold():
    allocation = { "SEB Europafond" : 0.5, "SEB Världenfond" : 0.5 }
    algo = BuyAndHold.BuyAndHold(allocation)
    return algo

def setup_rebalance():
    allocation = { "SEB Europafond" : 0.33, "SEB Världenfond" : 0.33 }
    algo = Rebalance.Rebalance(allocation)
    return algo

def setup_sma10():
    allocation = { "SEB Europafond" : 0.5, "SEB Världenfond" : 0.5 }
    algo = SMA10.SMA10(allocation)
    return algo

def setup_rel_mom(logger):
    allocation = { "SEB Europafond" : 0.5, "SEB Världenfond" : 0.5 }
    algo = RelativeMomentum.RelativeMomentum(allocation, True)
    algo.set_logger(logger)
    return algo

def test_collect():
    Utils.collect()

selected = ['SEB Aktiesparfond', 'SEB Emerging Marketsfond', 'SEB Europa Småbolag', 
            'SEB Europafond', 'SEB Fastighetsfond', 'SEB Japanfond', 
            'SEB Latinamerikafond', 'SEB Läkemedelsfond', 'SEB Nordamerika Småbolag', 
            'SEB Nordamerikafond', 'SEB Nordenfond', 'SEB Schweizfond', 
            'SEB Sverigefond', 'SEB Teknologifond', 'SEB Trygg Placeringsfond', 
            'SEB Världenfond']

funds = Utils.load_all(selected)

f = Factory.Factory()
logger = f.create_logger("log_rel_mom")

algo = setup_buy_and_hold()
ts1 = test_algo(funds, algo, logger, "AS")

algo = setup_rebalance()
ts2 = test_algo(funds, algo, logger, "AS")

algo = setup_sma10()
ts3 = test_algo(funds, algo, logger, "BMS")

algo = setup_rel_mom(logger)
ts4 = test_algo(funds, algo, logger, "BMS")


Utils.graph("TAA", ts1, ts2,ts3, ts4)

