import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter

import os

class SebGraphDisplay:
    def __init__(self, timeseries, graph_path):
        self._timeseries = timeseries
        self._graph_path = graph_path

    def execute(self):
        p = figure(plot_width=600, plot_height=200, x_axis_type="datetime")

        p.line(x = self._timeseries.index, y = self._timeseries.values, color='navy', alpha=0.5)

        #p.line(x = self._dataframe.index, y = self._dataframe.id.values, color='navy', alpha=0.5)

        p.xaxis.formatter=DatetimeTickFormatter(hours=["%Y %m %d"],
                                                days=["%Y %m %d"],
                                                months=["%Y %m %d"],
                                                years=["%Y %m %d"])

        filename = "{0}.html".format(self._timeseries.name)

        if not os.path.exists(self._graph_path):
            os.mkdir(self._graph_path)

        output_file(os.path.join(self._graph_path, filename))

        show(p)