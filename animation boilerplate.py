from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

WINDOW_X, WINDOW_Y = 20, 50  # upperleft coordinates of window
CANVAS_WIDTH, CANVAS_HEIGHT = 1300, 650
FPS = 60  # frames per second of animation

class Canvas(QLabel, object):
    def __init__(self, width, height):
        super(Canvas, self).__init__()  # TODO: find out what this does
        self.setPixmap(QPixmap(width, height))
        self.pixmap().fill(QColor(Qt.white))

    def clearAll(self):
        self.pixmap().fill(QColor(Qt.white))

class MainWindow(QMainWindow, object):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(WINDOW_X, WINDOW_Y, CANVAS_WIDTH, CANVAS_HEIGHT)  # position and dimensions of window
        self.setWindowTitle("PyQt Drawing")
        self.setWindowIcon(QIcon('pythonlogo.png'))
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)  # dimensions of canvas
        self.setCentralWidget(self.canvas)
        self.show()
        self.setup()

    def setup(self):
        # insert initial conditions for animation

        self.timer = QTimer()
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000 // FPS)

    def update(self):
        # code that executes between frames for animation
        pass

    def mainloop(self):
        self.canvas.clearAll()
        self.update()
        self.canvas.update()  # method that inherits from QLabel

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()