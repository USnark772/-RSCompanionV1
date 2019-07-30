# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar


class MyNavBar(NavBar):
    def __init__(self, figure, figure_parent):
        super().__init__(figure, figure_parent)

