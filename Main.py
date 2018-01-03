from datetime import date, datetime

import Factory as Factory

import Utils

import SebFundOperations

import Simulate

import BuyAndHold
import Rebalance

import Market

import Portfolio

import Evaluate

import Print

def test_algo():
    start = datetime(1999, 2, 26)
    end = datetime(2017, 10, 30)
    ops = SebFundOperations.SebFundOperations()

    funds = Utils.load_all(["SEB Europafond", "SEB Världenfond", "SEB Hedgefond"])

    #allocation = { "SEB Europafond" : 1.0}

    allocation = { "SEB Europafond" : 0.5, "SEB Världenfond" : 0.5 }

    #allocation = { "SEB Europafond" : 0.5 }

    #allocation = { "SEB Hedgefond" : 1.0 }

    #algo = BuyAndHold.BuyAndHold(allocation)
    algo = Rebalance.Rebalance(allocation)

    s = Simulate.Simulate(start, end)
    s.setup_reallocations(algo, "BAS")

    p = Portfolio.Portfolio(10000)

    f = Factory.Factory()
    logger = f.create_transaction_logger()
    m = Market.Market(funds, p, logger)

    ts = s.execute(m)

    #print(res)

    #Utils.graph(res)

    e = Evaluate.Evaluate(ts)
    result = e.execute()

    pr = Print.Print(result)
    pr.execute()

def test_collect():
    Utils.collect()


test_algo()
