
from ProcessOrders import ProcessOrders

class ProcessReallocations:
    class Reallocation:
        def __init__(self, fund_name, percentage):
            self.fund_name = fund_name
            self.target = percentage

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

    # calcs deviation from target (in percentage of portfolio value)
    def _deviation(self, date, realloc):
        percentage_funds = self._portfolio.calc_percentage(date, self._funds)

        deviation = realloc.target
        if realloc.fund_name in percentage_funds:
            current = percentage_funds[realloc.fund_name]
            deviation= realloc.target - current
        
        return deviation
    
    def _generate_order(self, date,  realloc):        
        if realloc.target == 0.0:
            # Keep nothing - sell everything in fund
            self._process_orders.add_sell_all_order(realloc.fund_name)
            return

        # How far from target are we?
        deviation = self._deviation(date, realloc)
        if round(deviation, 1) == 0.0:
            # Fund allocation already on target!
            return

        if deviation > 0:
            self._process_orders.add_buy_order(realloc.fund_name, deviation)
        else:
            self._process_orders.add_sell_order(realloc.fund_name, abs(deviation))
            
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
                self.add_reallocation(realloc.fund_name, realloc.target)

        # Finally process all sell orders to get cash
        self._process_orders.execute_sell_orders(date)
        # then process all buy orders
        self._process_orders.execute_buy_orders(date)
    

