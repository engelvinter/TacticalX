from ProcessOrder import ProcessOrder

class Market:
    class Order:
        def __init__(self, fund_name, percentage):
            self.fund_name = fund_name
            self.percentage = percentage

    def __init__(self, funds, portfolio):
        self._funds = funds
        self._portfolio = portfolio
        self._orders = []
        self._logger = None

    def place_order(self, fund_name, percentage_portfolio):
        self._orders.append(Market.Order(fund_name, percentage_portfolio))

    def register_transaction_logger(self, transaction_logger):
        self._logger = transaction_logger

    def _close_order(self, order):
        self._orders.remove(order)

    def order_depth(self):
        return len(self._orders)
        
    def process_orders(self, date):
        for order in self._orders[:]:
            # only process orders where fund has a quote of the actual date
            if date in self._funds[order.fund_name].index:
                p = ProcessOrder(date, self._funds, self._portfolio, self._logger)
                p.execute(order)
                self._close_order(order)

    #reallocate portfolio
    def update_portfolio(self, date, new_allocation):
        # Sell all funds not in new allocation to get cash
        fund_shares_portfolio = self._portfolio.get_all_fund_shares()

        for fund_name, shares in fund_shares_portfolio:
            if fund_name not in new_allocation:
                self.place_order(fund_name, 0.0)

        # Adjust the funds that we decide to keep
        for fund_name in new_allocation:
            self.place_order(fund_name, new_allocation[fund_name])

    def calc_portfolio_value(self, date):
        return self._portfolio.calc_value(date, self._funds)
    
    