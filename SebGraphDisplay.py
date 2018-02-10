import pandas as pd

from bokeh.plotting import figure, output_file, show, save
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import file_html

import os

class SebGraphDisplay:
    def __init__(self, title, graph_path):
        self._title = title
        self._graph_path = graph_path
        self._graph = self._setup_graph(title)

    def add_timeseries(self, timeseries, color):
         self._graph.line(x = timeseries.index, 
                          y = timeseries.values, 
                          legend = timeseries.name, 
                          color=color, 
                          alpha=0.5)

    def _setup_graph(self, name):
        graph = figure(title=name, plot_width=800, plot_height=400, x_axis_type="datetime")
        graph.xaxis.formatter = DatetimeTickFormatter(hours=["%Y %m %d"],
                                                            days=["%Y %m %d"],
                                                            months=["%Y %m %d"],
                                                            years=["%Y %m %d"])

        graph.legend.location = "top_left"

        return graph
    
    def create_file(self):
        filename = "graph.html"

        if not os.path.exists(self._graph_path):
            os.mkdir(self._graph_path)

        output_file(os.path.join(self._graph_path, filename))
        save(self._graph)

    def show(self):
        show(self._graph)