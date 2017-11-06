from datetime import date, datetime

import Factory as Factory

import Utils

import pandas as pd

import datetime as dt

import SebRebalance

import StratFactory

#if __name__ == "__main__":


funds = Utils.load_all(["SEB Europafond"])


r = StratFactory.create_buy_and_hold(funds)

p  = r.execute()

