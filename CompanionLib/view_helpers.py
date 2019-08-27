# A collection of commonly used code

from PySide2.QtWidgets import QFrame


class MyFrame(QFrame):
    """ Creates a frame for display purposes depending on bools. """
    def __init__(self, line=False, vert=False):
        super().__init__()
        if line:
            if vert:
                self.setFrameShape(QFrame.VLine)
            else:
                self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)
        else:
            self.setFrameShape(QFrame.StyledPanel)
            self.setFrameShadow(QFrame.Raised)

