
class Portfolio :
    def __init__(self, initial_investment):
        self._cash = initial_investment
        self._portfolio = {}   # name => nbr of shares

    def empty(self):
        return len(self._portfolio.keys()) is 0

    def get_all_fund_shares(self):
        return self._portfolio.items()

    def get_all_fund_names(self):
        return self._portfolio.keys()
    
    def fund_shares(self, fund_name):
        return self._portfolio[fund_name]
    
    def current_cash(self):
        return self._cash

    def invested_in_fund(self, fund_name):
        return fund_name in self._portfolio

    def increase_fund(self, fund_name, shares):
        if fund_name in self._portfolio:
            self._portfolio[fund_name] += shares
        else:
            self._portfolio[fund_name] = shares

    def decrease_fund(self, fund_name, shares):
        if fund_name not in self._portfolio:
            raise Exception("Cannot decrease {0} since it does not exist in portfolio".format(fund_name))

        if self._portfolio[fund_name] < shares:
            raise Exception("Cannot decrease {0} with {1} shares (only {2} left)".format(fund_name, shares, self._portfolio[fund_name]))

        self._portfolio[fund_name] -= shares
        
        # If fund down to zero i.e remove fund from portfolio
        if self._portfolio[fund_name] == 0.0:
            del self._portfolio[fund_name]

    def increase_cash(self, amount):
        self._cash += amount
    
    def decrease_cash(self, amount):
        if self._cash < amount:
            raise Exception("Cannot decrease cash with {0} (only {1} left)", amount, self._cash)

        self._cash -= amount

    class CalcValueException(Exception):
        pass

    def calc_value(self, date, funds):
        value = {}
        value['cash'] = self.current_cash()
        all_shares = self.get_all_fund_shares()

        try:
            for fund_name, shares in all_shares:
                quote = funds[fund_name].loc[date].quote
                fund_value = shares * quote
                value[fund_name] = fund_value
        except KeyError:
            raise Portfolio.CalcValueException("Not able to calculate any value {0}", date)

        return value

    def calc_percentage(self, date, funds):
        value = self.calc_value(date, funds)
        tot_value = sum(value.values())

        percentage = {}
        for fund_name, fund_value in value.items():
            percentage[fund_name] = fund_value / tot_value

        return percentage