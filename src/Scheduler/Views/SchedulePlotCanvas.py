import Scheduler.Views.plot_gantt as plot_gantt

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

'''
Canvas for plts
'''
class SchedulePlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.data = data

        self.compute_figure(self.data)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)

    '''
    Compute the figure

    Args:
        Object data: The schedule data
    '''
    def compute_figure(self, data):
        if data is None:
            return

        self.data = data
        plot_gantt.plot_gantt(self.fig, self.axes, self.data)

    '''
    Compute and save figure, NOTE backed by matplotlib not pyqt5

    Args:
        Str path: The filename to save the figure
    '''
    def save_figure(self, path):
        fig, axes = plt.subplots(nrows=1, ncols=1)
        plot_gantt.plot_gantt(fig, axes, self.data)
        fig.savefig(path)
