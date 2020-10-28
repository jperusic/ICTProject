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

    ## Function for Plot to display on the graph as a line rather than scatter - two can be altered between in system
    def plot_line(self, data: list, title: str = 'Normalised Spectra Plot'):
        """This is the function for plotting a LINE PLOT"""
        ## Takes the first row of the data set to be plotted and checks how many columns the row has, used to determine no of spectra values to plot
        row0 = data[0]
        cols = len(row0)
        self.ax.cla()

        ## If only a single spectra value in the dataset seperate as wave and spectra
        if cols == 2:
            wave = [i[0] for i in data]
            sp = [i[1] for i in data]

            ## Plot the wave and spectra x 1 data on the graph as smooth line plot
            self.ax.plot(wave, sp, label='Spectra')

        ## If there are two spectra values in the dataset seperate as wave, spectra1 and spectra2   
        elif cols == 3:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]

            ## Plot the wave and spectra x 2 data on the graph as smooth line plot
            self.ax.plot(wave, sp1, label='Spectra 1')
            self.ax.plot(wave, sp2, label='Spectra 2')

        ## If there are three spectra values in the dataset seperate as wave, spectra1, spectra2 and spectra3  
        elif cols == 4:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]
            sp3 = [i[3] for i in data]

            ## Plot the wave and spectra x 3 data on the graph as smooth line plot
            self.ax.plot(wave, sp1, label='Spectra 1')
            self.ax.plot(wave, sp2, label='Spectra 2')
            self.ax.plot(wave, sp3, label='Spectra 3')

        ## Catch errors for incorrect format encounters
        else:
            raise ValueError

        ## Set the title of the graph to show the dynamically generated text based on selected file
        ## Label the axis of the graph, consistantly used - X = Waves and Y = Spectra Values
        ## Include the legend in the graph and dispaly the generated graph to the user
        self.ax.set_title(title)
        self.ax.set_xlabel('Wave Shift (cm -1)')
        self.ax.set_ylabel('Intensity (arb.)')
        self.ax.legend()

        self.draw()

    ## Function for Plot to display on the graph as a scatter rather than line - two can be altered between in system
    def plot_scatter(self, data: list, title: str = 'Normalised Spectra Plot'):
        """This is the function for plotting a SCATTER PLOT """
        ## Takes the first row of the data set to be plotted and checks how many columns the row has, used to determine no of spectra values to plot
        row0 = data[0]
        cols = len(row0)
        self.ax.cla()

        ## If only a single spectra value in the dataset seperate as wave and spectra
        if cols == 2:
            wave = [i[0] for i in data]
            sp = [i[1] for i in data]

            ## Plot the wave and spectra x 1 data on the graph as scatter plot with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp, label='Spectra', marker=".", linewidths=0)


        ## If there are two spectra values in the dataset seperate as wave, spectra1 and spectra2   
        elif cols == 3:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]

            ## Plot the wave and spectra x 2 data on the graph as scatter plot with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.scatter(wave, sp2, label='Spectra 2', marker=".", linewidths=0)

        ## If there are three spectra values in the dataset seperate as wave, spectra1, spectra2 and spectra3  
        elif cols == 4:
            wave = [i[0] for i in data]
            sp1 = [i[1] for i in data]
            sp2 = [i[2] for i in data]
            sp3 = [i[3] for i in data]

            ## Plot the wave and spectra x 3 data on the graph as scatter plot with small points - easier to distinguish on graph
            self.ax.scatter(wave, sp1, label='Spectra 1', marker=".", linewidths=0)
            self.ax.scatter(wave, sp2, label='Spectra 2', marker=".", linewidths=0)
            self.ax.scatter(wave, sp3, label='Spectra 3', marker=".", linewidths=0)

        ## Catch errors for incorrect format encounters
        else:
            raise ValueError

        ## Set the title of the graph to show the dynamically generated text based on selected file
        ## Label the axis of the graph, consistantly used - X = Waves and Y = Spectra Values
        ## Include the legend in the graph and dispaly the generated graph to the user
        self.ax.set_title(title)
        self.ax.set_xlabel('Wave Shift (cm -1)')
        self.ax.set_ylabel('Intensity (arb.)')
        self.ax.legend()

        self.draw()

    ## Function to clear the plot shown on the graph - Reverts to blank so other plots can be displayed
    def plot_clear(self):
        """clear a plot-"""
        self.ax.cla()
        self.draw()
