from datetime import date, datetime, timedelta

import pandas as pd

import SebRebalance

def create_buy_and_hold(funds):
    fixed_alloc = { "SEB Europafond" : 1.0}

    range_start = datetime(1999, 2, 26)
    range_end = datetime(2017, 10, 30)

    # First get the periodical time series
    range = pd.date_range(start=range_start, end=range_end, freq='AS').tolist()
    # Insert end values
    range.insert(0, range_start)
    range.append(range_end)

    # Make a shorter periodical series
    short_range = range[:-1]

    # First reverse the two time series - they begin at different dates 
    # since we removed the last date in short_range
    # Then zip the two series making tuples containing start and end value of a period
    periodIter = zip(reversed(range), reversed(short_range))
    
    alloc = None
    next = None
    # Make a linked list of Rebalance objects, returning the last
    for end, start in periodIter:
        alloc = SebRebalance.SebRebalance(funds, fixed_alloc, start, end, next)
        next = alloc
    
    return alloc