
class Print:
    def __init__(self, result):
        self._result = result

    def _print_total(self):
        print("Total return: {:.1f}%".format(self._result.total))
    
    def _print_yearly(self):
        print("Yearly: ")
        for date in self._result.yearly:
            print("{} {:.1f}%".format(date.strftime("%Y"), self._result.yearly[date]))

    def _print_summary_quarter(self):
        pos = 0
        neg = 100
        for quarter in self._result.quarterly:
            res = self._result.quarterly[quarter]
            if res < neg:
                neg = res
            if res > pos:
                pos = res
        print("Worst quarter: {:.1f}%".format(neg))
        print("Best quarter:  {:.1f}%".format(pos))

    def _print_worst_drawdown(self):
        neg = 100
        temp = 0
        for month in self._result.monthly:
            res = self._result.monthly[month]
            if res < 0:
                temp += res
            if res >= 0:
                if temp < neg:
                    neg = temp
                temp = 0
        print("Worst drawdown: {:.1f}%".format(neg))

    def execute(self):
        self._print_total()
        self._print_yearly()
        self._print_summary_quarter()
        self._print_worst_drawdown()