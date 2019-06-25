import sys
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random


class main_window(QTabWidget):
    def __init__(self, parent=None):
        super(main_window, self).__init__(parent)

        # GUI configuration
        self.tab1 = QWidget()
        self.addTab(self.tab1, "Tab 1")
        self.figure = plt.figure(figsize=(10, 5))
        self.resize(800, 480)
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(10)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
