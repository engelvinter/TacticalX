import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter

import os

class SebGraphDisplay:
    def __init__(self, title, graph_path):
        self._title = title
        self._graph_path = graph_path
        self._graph = self._create_graph(title)

    def _create_graph(self, name):
        graph = figure(title=name, plot_width=800, plot_height=400, x_axis_type="datetime")
        return graph

    def add_timeseries(self, timeseries, color):
         self._graph.line(x = timeseries.index, 
                          y = timeseries.values, 
                          legend = timeseries.name, 
                          color=color, 
                          alpha=0.5)

    def show(self):
        
        self._graph.xaxis.formatter = DatetimeTickFormatter(hours=["%Y %m %d"],
                                                            days=["%Y %m %d"],
                                                            months=["%Y %m %d"],
                                                            years=["%Y %m %d"])

        self._graph.legend.location = "top_left"

        filename = "{0}.html".format(self._title)

        if not os.path.exists(self._graph_path):
            os.mkdir(self._graph_path)

        output_file(os.path.join(self._graph_path, filename))

        show(self._graph)