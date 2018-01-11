from datetime import date, datetime

import Factory as Factory

import Utils

import SebFundOperations

import Simulate

import BuyAndHold
import Rebalance
import SMA10

import Market

import Portfolio

import Evaluate

import Print

def test_algo(funds, algo, freq):
    start = datetime(2000, 2, 26)
    end = datetime(2017, 10, 30)
    ops = SebFundOperations.SebFundOperations()
  
    s = Simulate.Simulate(start, end)
    s.setup_reallocations(algo, freq)

    p = Portfolio.Portfolio(10000)

    f = Factory.Factory()
    logger = f.create_transaction_logger()
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

def test_collect():
    Utils.collect()

funds = Utils.load_all(["SEB Europafond", "SEB Världenfond", "SEB Hedgefond"])

algo = setup_buy_and_hold()
ts1 = test_algo(funds, algo, "AS")

algo = setup_rebalance()
ts2 = test_algo(funds, algo, "AS")

algo = setup_sma10()
ts3 = test_algo(funds, algo, "BMS")

Utils.graph("TAA", ts1, ts2, ts3)

