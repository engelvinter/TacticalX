
from Portfolio import Portfolio
from SebFundOperations import SebFundOperations

import math

class ProcessOrders:
    class Order:
        def __init__(self, fund_name, percentage):
            self.fund_name = fund_name
            self.percentage = percentage

    def __init__(self, funds, portfolio, logger = None):
        self._portfolio = portfolio
        self._funds = funds
        self._logger = logger
        self._buy_orders = []
        self._sell_orders = []
        self._fund_ops = SebFundOperations()

    def add_buy_order(self, fund_name, percentage):
        order = ProcessOrders.Order(fund_name, percentage)
        self._buy_orders.append(order)
    
    def add_sell_order(self, fund_name, percentage):
        order = ProcessOrders.Order(fund_name, percentage)
        self._sell_orders.append(order)

    def add_sell_all_order(self, fund_name):
        order = ProcessOrders.Order(fund_name, float('nan'))
        self._sell_orders.append(order)

    def _log_warning(self, date, fund_name, initial_amount, amount):
        if self._logger is None:
            return

        self._logger.warning("%s Warning: Decreased amount in %s from %.1f to %.1f because of cash shortage",
                             date.strftime('%Y-%m-%d'),
                             fund_name, 
                             initial_amount, 
                             amount)

    def _log_closed_order(self, date, text, fund_name, amount):
        if self._logger is None:
            return
        
        self._logger.info("%s %s %s %d Skr", 
                          date.strftime('%Y-%m-%d'), 
                          text, 
                          fund_name, 
                          amount)

    def _calc_value_of_portfolio(self, date, percentage):
        value = self._portfolio.calc_value(date, self._funds)
        total_value = sum(value.values())

        amount = percentage * total_value

        return round(amount, 2)

    def _decrease_cash(self, value):
        # Since we are buying, first decrease cash to get money
        try:
            self._portfolio.decrease_cash(value)
        except Portfolio.OverdrawOfCash:
            # Ok, not enough left, might be rounding error
            # Withdraw what we have in cash
            cash = self._portfolio.take_all_cash()
            value = cash
        
        return value

    def _buy_fund(self, date, fund_name, value):
        fund = self._funds[fund_name]
        # Calc nbr of shares
        shares = self._fund_ops.calc_shares(fund, date, value)
        # then "buy" and increase the shares of the fund
        self._portfolio.increase_fund(fund_name, shares)

        self._log_closed_order(date, "Bought", fund_name, value)

    def _execute_buy_order(self, date, order):
        value = self._calc_value_of_portfolio(date, order.percentage)
        value = self._decrease_cash(value)        
        self._buy_fund(date, order.fund_name, value)

    def _sell_fund(self, date, fund_name, fund):
        shares = self._portfolio.close_fund(fund_name)
        value = self._fund_ops.calc_value(fund, date, shares)
        return value

    def _sell_part_of_fund(self, date, fund_name, fund, percentage):
        value = self._calc_value_of_portfolio(date, percentage)

        # First calc nbr of shares
        shares = self._fund_ops.calc_shares(fund, date, value)

        # Since we are selling, first "sell" and decrease the shares of the fund
        try:
            self._portfolio.decrease_fund(fund_name, shares)
        except:
            # Ok, not enough shares left, might be rounding error
            # Take all shares left in that fund
            value = self._sell_fund(date, fund_name, fund)

        return value

    def _execute_sell_order(self, date, order):
        fund = self._funds[order.fund_name]

        if math.isnan(order.percentage):
            value = self._sell_fund(date, order.fund_name, fund)
        else:
            value = self._sell_part_of_fund(date, order.fund_name, fund, order.percentage)
            
        # then increase cash
        self._portfolio.increase_cash(value)

        self._log_closed_order(date, "Sold", order.fund_name, value)

    def execute_sell_orders(self, date):
        for order in self._sell_orders:
            self._execute_sell_order(date, order)
        self._sell_orders = []

    def execute_buy_orders(self, date):
        for order in self._buy_orders:
            self._execute_buy_order(date, order)
        self._buy_orders = []
    
