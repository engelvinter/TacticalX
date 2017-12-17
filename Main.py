from datetime import date, datetime

import Factory as Factory

import Utils

import SebRebalance

import StrategyFactory

import SebFundOperations

import Simulate

import BuyAndHold

import Market

import Portfolio


#if __name__ == "__main__":

start = datetime(1999, 2, 26)
end = datetime(2017, 10, 30)
ops = SebFundOperations.SebFundOperations()

funds = Utils.load_all(["SEB Europafond", "SEB Världenfond"])
ops.add_cash(funds, start, end)

#allocation = { "SEB Europafond" : 1.0}

#allocation = { "SEB Europafond" : 0.5, "SEB Världenfond" : 0.5 }

allocation = { "SEB Europafond" : 0.5, "Cash" : 0.5 }

s = Simulate.Simulate(start, end)
algo = BuyAndHold.BuyAndHold(allocation)
s.setup_reallocations(algo, "BAS")

p = Portfolio.Portfolio(10000)

f = Factory.Factory()
logger = f.create_transaction_logger()
m = Market.Market(funds, p)
m.register_transaction_logger(logger)

res = s.execute(m)

print(res)

Utils.graph(res)

