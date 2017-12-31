
from ProcessOrders import ProcessOrders

class ProcessReallocations:
    class Reallocation:
        def __init__(self, fund_name, percentage):
            self.fund_name = fund_name
            self.percentage = percentage

    def __init__(self, funds, portfolio, logger = None):
        self._funds = funds
        self._portfolio = portfolio
        self._logger = logger
        self._reallocations = []
        self._process_orders = ProcessOrders(funds, portfolio, logger)

    def add_reallocation(self, fund_name, percentage):
        realloc = ProcessReallocations.Reallocation(fund_name, percentage)
        self._reallocations.append(realloc)

    def _reinit_allocations(self):
        self._reallocations = []

    def _target_delta(self, date, realloc):
        current_percentage = self._portfolio.calc_percentage(date, self._funds)

        delta = realloc.percentage
        if realloc.fund_name in current_percentage:
            delta = realloc.percentage - current_percentage[realloc.fund_name]
        
        return delta

    def _calc_amount(self, date, target_delta):
        value = self._portfolio.calc_value(date, self._funds)
        total_value = sum(value.values())

        amount = target_delta * total_value

        return amount

    def _generate_order(self, date,  realloc):
        # How far from target are we?
        target_delta = self._target_delta(date, realloc)
        if target_delta == 0.0:
            # Fund allocation already on target!
            return
        
        # How much is this delta in portfolio value?
        amount = round(self._calc_amount(date, target_delta), 1)

        if amount > 0:
            self._process_orders.add_buy_order(realloc.fund_name, amount)
        else:
            self._process_orders.add_sell_order(realloc.fund_name, abs(amount))
            
    def execute(self, date):
        if not self._reallocations:
            return

        work_list = self._reallocations
        self._reinit_allocations()

        # First preprocess by generating all orders
        while work_list:
            realloc = work_list.pop()
            if date in self._funds[realloc.fund_name].index:
                self._generate_order(date, realloc)
            else:
                # Put back into reallocation queue
                self.add_reallocation(realloc.fund_name, realloc.percentage)

        # Finally process all sell orders to get cash
        self._process_orders.execute_sell_orders(date)
        # then process all buy orders
        self._process_orders.execute_buy_orders(date)
    

