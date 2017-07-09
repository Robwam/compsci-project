import Scheduler.Views.plot_gantt as plot_gantt

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import logging
logger = logging.getLogger(__name__)

class SchedulePlotCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.compute_figure(data)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolic(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_figure(self, data):
        if data is None:
            return
        #   # TODO this is test data, should be real, duh
        #   ylabels, effort, task_dates, pos = plot_gantt.test_data()
        plot_gantt.plot_gantt(self.fig, self.axes, data)
