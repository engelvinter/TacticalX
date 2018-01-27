
class Print:
    def __init__(self, result):
        self._result = result

    def _print_total(self):
        print("Total return: {:.1f}%".format(self._result.total))
    
    def _print_yearly(self):
        yearly_formated = self._result.yearly.round(1).astype(str) + '%'
        print("Yearly: ")
        print(yearly_formated)

    def _print_worst(self):    
        print("Worst drawdown: {:.1f}%".format(self._result.drawdown))
        print("Worst year: {:.1f}%".format(self._result.yearly.min()))
        print("Worst month: {:.1f}%".format(self._result.monthly.min()))

    def execute(self):
        self._print_total()
        self._print_yearly()
        self._print_worst()