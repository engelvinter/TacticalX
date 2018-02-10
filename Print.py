import sys

class Print:
    def __init__(self, result):
        self._result = result
        self._result_path = None
        self._file_path = None

    def add_file_output(self, file_path):
        self._file_path = file_path

    def _print_total(self):
        print("Total return: {:.1f}%".format(self._result.total))
        print("CAGR: {:.1f}%".format(self._result.cagr))

    def _print_yearly(self):
        yearly_formated = self._result.yearly.round(1).astype(str) + '%'
        print("Yearly: ")
        print(yearly_formated)

    def _print_worst(self):    
        print("Worst drawdown: {:.1f}%".format(self._result.drawdown))
        print("Worst year: {:.1f}%".format(self._result.yearly.min()))
        print("Worst month: {:.1f}%".format(self._result.monthly.min()))

    def _header(self):
        print("----------------------------------------------------------------")

    def _print_result(self):
        self._header()
        self._print_total()
        self._print_yearly()
        self._print_worst()

    def execute(self):
        self._print_result()
        if self._file_path:
            tmp = sys.stdout
            sys.stdout = open(self._file_path, "w")
            self._print_result()
            sys.stdout.close()
            sys.stdout = tmp