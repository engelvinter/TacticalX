
class ProcessOrder:
    def __init__(self, date, funds, portfolio, transaction_logger = None):
        self._date = date
        self._funds = funds
        self._portfolio = portfolio
        self._logger = transaction_logger

    def _calc_shares(self, fund_name, amount):
        quote = self._funds[fund_name].loc[self._date].quote
        shares = amount / quote
        return shares

    def _buy(self, fund_name, amount):
        # First calc nbr of shares
        shares = self._calc_shares(fund_name, amount)
        # Since we are buying, first decrease cash
        self._portfolio.decrease_cash(amount)
        # then "buy" and increase the shares of the fund
        self._portfolio.increase_fund(fund_name, shares)
    
    def _sell(self, fund_name, amount):
         # First calc nbr of shares
        shares = self._calc_shares(fund_name, amount)
        # Since we are selling, first "sell" and decrease the shares of the fund
        self._portfolio.decrease_fund(fund_name, shares)
        # then increase cash
        self._portfolio.increase_cash(amount)

    def _target_delta(self, order):
        current_percentage = self._portfolio.calc_percentage(self._date, self._funds)

        delta = order.percentage
        if order.fund_name in current_percentage:
            delta = order.percentage - current_percentage[order.fund_name]
        
        return delta

    def _calc_amount(self, target_delta):
        value = self._portfolio.calc_value(self._date, self._funds)
        total_value = sum(value.values())

        amount = target_delta * total_value

        return amount

    def _log_transaction(self, fund_name, target_delta):
        if self._logger is None:
            return
        
        date_str = self._date.strftime("%Y-%m-%d")
        if target_delta > 0:
            self._logger.info("%s : Increase by %.1f%% of %s", date_str, 100 * target_delta, fund_name)
        else:
            self._logger.info("%s : Decrease by %.1f%% of %s", date_str, 100 * abs(target_delta), fund_name)

    def execute(self, order):        
        target_delta = self._target_delta(order)
        if target_delta == 0.0:
            # fund allocation already achieved
            return

        amount = self._calc_amount(target_delta)

        if amount > 0:
            self._buy(order.fund_name, amount)
        else:
            self._sell(order.fund_name, abs(amount))

        self._log_transaction(order.fund_name, target_delta)