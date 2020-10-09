import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as _CanvasWidget
from matplotlib.figure import Figure
from matplotlib.backend_bases import PickEvent


class CanvasWidget(_CanvasWidget):
    sig_picked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(figure)
        self.ax = figure.add_subplot(111)

    def plot_data(self, data: list, typo: str, title: str = 'Normalised Spectra Plot'):
        """
        Plot Data
        :param data: the data to plot, a list of many rows, each row has exact same columns.
        :param typo: ether "line" or "scatter". This param tells you what kind of plot user is expecting.
        :param title: title of the plot
        :return:
        """
        if typo == 'line':
            return self.plot_line(data=data, title=title)
        elif typo == 'scatter':
            return self.plot_scatter(data=data, title=title)

    def plot_line(self, data: list, title: str = 'Normalised Spectra Plot'):
        """This is the function for plotting a LINE PLOT"""

        row0 = data[0]
        cols = len(row0)
        self.ax.cla()
        if cols == 2:
            wave = [i[0] for i in data]
            sp = [i[1] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.plot(wave, sp, label='Spectra', marker=".",  # linewidths=0
                         )

        elif cols == 3:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.plot(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.plot(wave, sp2, label='Spectra 2', marker=".", linewidths=0)

        elif cols == 4:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]
            sp3 = [i[3] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.plot(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.plot(wave, sp2, label='Spectra 2', marker=".", linewidths=0)
            self.ax.plot(wave, sp3, label='Spectra 3', marker=".", linewidths=0)

        else:
            raise ValueError
        self.ax.set_title(title)
        self.ax.set_xlabel('Wavelength')
        self.ax.set_xlabel('Spectra')
        self.ax.legend()

        self.draw()

    def plot_scatter(self, data: list, title: str = 'Normalised Spectra Plot'):
        """This is the function for plotting a SCATTER PLOT """

        row0 = data[0]
        cols = len(row0)
        self.ax.cla()
        if cols == 2:
            wave = [i[0] for i in data]
            sp = [i[1] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp, label='Spectra', marker=".", linewidths=0)

        elif cols == 3:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.scatter(wave, sp2, label='Spectra 2', marker=".", linewidths=0)

        elif cols == 4:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]
            sp3 = [i[3] for i in data]

            ## display graph as scatter with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.scatter(wave, sp2, label='Spectra 2', marker=".", linewidths=0)
            self.ax.scatter(wave, sp3, label='Spectra 3', marker=".", linewidths=0)

        else:
            raise ValueError
        self.ax.set_title(title)
        self.ax.set_xlabel('Wavelength')
        self.ax.set_ylabel('Spectra')
        self.ax.legend()

        self.draw()

    def plot_clear(self):
        """clear a plot-"""
        self.ax.cla()
        self.draw()