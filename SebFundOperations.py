
import re

import pandas as pd

from DateUtil import assign_date, str_format

import datetime

class SebFundOperations:
    def __init__(self):
        pass
    
    def get_interval(self, fund):
        fund_start = fund.iloc[0].name
        fund_end = fund.iloc[-1].name
        
        return fund_start, fund_end

    def filter_interval(self, funds, start, end):
        available_funds = []
        for name in funds:
            fund = funds[name]
            (fund_start, fund_end) = self.get_interval(fund)
            if start >= fund_start and end <= fund_end:
                available_funds.append(name)

        return available_funds

    # regexp
    # .*  - any alfacharacter
    # $   - end
    # ^   - start
    # SEB - All that starts with SEB 
    def filter_name(self, funds, regexp):
        filtered_funds = []
        for name in funds:
            if re.match(regexp, name):
                filtered_funds.append(name)
                
        return filtered_funds

    # get all funds up to a certain date
    def get_available_funds(self, date, funds):
        date = assign_date(date)
        avail = {}
        
        for fund_name in funds:
            fund = funds[fund_name]
            start, end = self.get_interval(fund)
            if start < date and end >= date:
                try:
                    idx = fund.index.get_loc(date, method='bfill')
                    # + 1 since we want to include the last date
                    avail[fund_name] = fund.iloc[:idx + 1]   
                except ValueError:
                    print("Index error (unordered): {}".format(fund_name))

        return avail

    class NoData(Exception):
        pass

    # Calc the return at the given date starting from nbr_days back in time
    def current_return(self, date, fund, nbr_days):
        date = assign_date(date)

        # First check that current date (arg) is not after end date of fund
        start_date_fund, end_date_fund = self.get_interval(fund)
        if date > end_date_fund:
            str = "The date {} is after the end date of fund ({})".format(str_format(date),
                                                                          str_format(end_date_fund))
            raise SebFundOperations.NoData(str)

        # then check that the start date of the evaluation is not before start date of fund
        start_date = date - datetime.timedelta(nbr_days)
        if start_date <= start_date_fund:
            str = "The date {} is before the start date of fund ({})".format(str_format(start_date),
                                                                             str_format(start_date_fund))
            raise SebFundOperations.NoData(str)

        current_idx = fund.index.get_loc(date, method='bfill')
        start_idx = fund.index.get_loc(start_date, method='bfill')
        ret = fund.iloc[current_idx].quote / fund.iloc[start_idx].quote - 1.0
        return ret

    # For all funds - Calc the return at the given date starting from nbr_days back in time
    # Skip those funds that do not have any data during the interval
    def current_return_funds(self, date, funds, nbr_days):
        performance = {}
        avail = self.get_available_funds(date, funds)
        for fund_name in avail:
            try:
                fund = avail[fund_name]
                ret = self.current_return(date, fund, nbr_days)
                performance[fund_name] = ret
            except SebFundOperations.NoData:
                pass

        return performance.items()

    def calc_shares(self, fund, date, value):
        quote = fund.loc[date].quote
        shares = value / quote
        return shares

    def calc_value(self, fund, date, shares):
        quote = fund.loc[date].quote
        value = shares * quote
        return round(value, 2)
         
            

                
