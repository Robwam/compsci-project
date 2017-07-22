import Scheduler.Views.plot_gantt as plot_gantt

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import logging
logger = logging.getLogger(__name__)

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
# ax.plot([0,1,2], [10,20,3])
# fig.savefig('path/to/save/image/to.png')   # save the figure to file
# plt.close(fig)

class SchedulePlotCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.data = data

        self.compute_figure(self.data)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        #FigureCanvas.setSizePolic(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_figure(self, data):
        if data is None:
            return

        self.data = data
        #   # TODO this is test data, should be real, duh
        #   ylabels, effort, task_dates, pos = plot_gantt.test_data()
        plot_gantt.plot_gantt(self.fig, self.axes, self.data)



    def save_figure(self, path):
        # Compute and save figure, NOTE backed by matplotlib not pyqt5
        fig, axes = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        plot_gantt.plot_gantt(fig, axes, self.data)
        fig.savefig(path)
