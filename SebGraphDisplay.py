import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter

class SebGraphDisplay:
    def __init__(self, dataframe, graph_path):
        self._dataframe = dataframe
        self._graph_path = graph_path

    def execute(self):
        p = figure(plot_width=600, plot_height=200, x_axis_type="datetime")

        p.line(x = self._dataframe.index, y = self._dataframe.quote.values, color='navy', alpha=0.5)

        #p.line(x = self._dataframe.index, y = self._dataframe.id.values, color='navy', alpha=0.5)

        p.xaxis.formatter=DatetimeTickFormatter(hours=["%Y %m %d"],
                                                days=["%Y %m %d"],
                                                months=["%Y %m %d"],
                                                years=["%Y %m %d"])

        output_file("{0}/{1}.html".format(self._graph_path, self._dataframe.name))

        show(p)