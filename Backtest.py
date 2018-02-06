from DateUtil import assign_date

from Simulate import Simulate

from Portfolio import Portfolio

from Market import Market

from Evaluate import Evaluate

class Backtest:
    def __init__(self, name, algo, freq, funds):
        self._name = name
        self._algo = algo
        self._freq = freq
        self._funds = funds
        self._logger = None
    
    def set_logger(self, logger):
        self._logger = logger

    def _create_simulate(self, start, end):
        s = Simulate(start, end)
        s.setup_reallocations(self._algo, self._freq)
        return s
    
    def _create_market(self, funds):
        p = Portfolio(10000)
        m = Market(funds, p, self._logger)
        return m
        
    def execute(self, start, end):
        start = assign_date(start)
        end = assign_date(end)

        market = self._create_market(self._funds)
        simulate = self._create_simulate(start, end)

        ts = simulate.execute(market)
        ts.name = self._name

        e = Evaluate(ts)
        result = e.execute()

        return ts, result