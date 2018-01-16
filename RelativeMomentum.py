
from SebFundOperations import SebFundOperations

class RelativeMomentum:
    def __init__(self, default_allocation):
        self._default = default_allocation
        self._initial_investing_done = False
        self._fund_op = SebFundOperations()
        self.name = "Relative Momentum"

    def execute(self, date, market):
        if self._initial_investing_done is False:
            # Do inital investment
            market.update_portfolio(date, self._default)
            self._initial_investing_done = True
            return

        ret_funds = self._fund_op.current_return_funds(date, 
                                                       market.get_available_funds(date), 
                                                       21)                                                
        new_alloc = {}
        ret_sorted = sorted(ret_funds, key=lambda x:x[1], reverse=True)
        #print("*", len(ret_sorted))
        for fund_name, _ in ret_sorted[0:4]:
            new_alloc[fund_name] = 0.20
        
        #print(new_alloc)
        market.update_portfolio(date, new_alloc)



        
