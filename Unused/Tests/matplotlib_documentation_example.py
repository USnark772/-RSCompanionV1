import sys
import time

import numpy as np

from PySide2.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication
from PySide2.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Plots(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.static_canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(NavigationToolbar(self.static_canvas, self))

        self.dynamic_canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.dynamic_canvas)
        self.layout.addWidget(NavigationToolbar(self.dynamic_canvas, self))

        self._static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._timer = self.dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Plots())


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
