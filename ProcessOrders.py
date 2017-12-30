
class ProcessOrders:
    class Order:
        def __init__(self, fund_name, amount):
            self.fund_name = fund_name
            self.amount = amount

    def __init__(self, funds, portfolio, logger = None):
        self._portfolio = portfolio
        self._funds = funds
        self._logger = logger
        self._buy_orders = []
        self._sell_orders = []

    def add_buy_order(self, fund_name, amount):
        order = ProcessOrders.Order(fund_name, amount)
        self._buy_orders.append(order)
    
    def add_sell_order(self, fund_name, amount):
        order = ProcessOrders.Order(fund_name, amount)
        self._buy_orders.append(order)
    
    def _calc_shares(self, fund_name, date, amount):
        quote = self._funds[fund_name].loc[date].quote
        shares = amount / quote
        return shares

    def _log_warning(self, fund_name, initial_amount, amount):
        if self._logger is None:
            return

        self._logger.warning("Warning: Decreased amount in %s from %d to %d because of cash shortage", 
                             fund_name, 
                             initial_amount, 
                             amount)

    def _log_closed_order(self):
        if self._logger is None:
            return
        pass

    def _execute_buy_order(self, date, order):
        # First calc nbr of shares
        shares = self._calc_shares(order.fund_name, date, order.amount)
        # Since we are buying, first decrease cash
        self._portfolio.decrease_cash(order.amount)
        # then "buy" and increase the shares of the fund
        self._portfolio.increase_fund(order.fund_name, shares)

    def _execute_sell_order(self, date, order):
         # First calc nbr of shares
        shares = self._calc_shares(order.fund_name, date, order.amount)
        # Since we are selling, first "sell" and decrease the shares of the fund
        self._portfolio.decrease_fund(order.fund_name, shares)
        # then increase cash
        self._portfolio.increase_cash(order.amount)

    def execute_sell_orders(self, date):
        for order in self._sell_orders:
            self._execute_sell_order(date, order)
        self._sell_orders = []

    def execute_buy_orders(self, date):
        for order in self._buy_orders:
            if order.amount > self._portfolio.current_cash():
                old_amount = order.amount
                order.amount = self._portfolio.current_cash()
                self._log_warning(order.fund_name, old_amount, order.amount)

            self._execute_buy_order(date, order)
        self._buy_orders = []
    
