from datetime import date, datetime

import Factory as Factory

import Utils

import SebRebalance

import StrategyFactory

import SebFundOperations

#if __name__ == "__main__":

start = datetime(1999, 2, 26)
end = datetime(2017, 10, 30)
ops = SebFundOperations.SebFundOperations()

funds = Utils.load_all(["SEB Europafond"])
ops.add_cash(funds, start, end)

allocation = { "SEB Europafond" : 1.0}
sf = StrategyFactory.StrategyFactory(funds, start, end)
r = sf.create_rebalanced(allocation)

portfolio = { "SEB Europafond" : 100 }
p = r.execute(portfolio)
