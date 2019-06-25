
import sys
import time
import numpy as np

from datetime import datetime, timedelta
from random import gauss
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy


class GraphObj(QFrame):
    def __init__(self, name):
        super().__init__()
        self.__name = name

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFixedHeight(400)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.setLayout(QVBoxLayout())

        # make up some data
        self.x = [datetime.now() + timedelta(hours=i) for i in range(12)]
        self.y = [i + gauss(0, 1) for i, _ in enumerate(self.x)]

        # plot
        plt.plot(self.x, self.y)
        # beautify the x-labels
        plt.gcf().autofmt_xdate()

        plt.show()
