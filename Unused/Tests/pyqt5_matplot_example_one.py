import sys
from random import gauss
from datetime import datetime, timedelta
from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy, QFrame, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.frame.setLayout(QHBoxLayout())
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.setCentralWidget(self.frame)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        m = PlotCanvas(self, width=5, height=4)
        self.frame.layout().addWidget(m)
        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.my_fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.my_fig)
        self.axes = None
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot()

    def plot(self):
        # data = [random.random() for i in range(25)]
        x = [datetime.now() + timedelta(hours=i) for i in range(12)]
        y = [i + gauss(0, 1) for i, _ in enumerate(x)]

        self.axes = self.figure.add_subplot(111)
        self.figure.autofmt_xdate()
        # self.axes.plot(data, 'r-')
        self.axes.plot(x, y)
        self.axes.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
