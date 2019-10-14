from PyQt5.QtCore import QDate, QLocale, Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QTextCharFormat, QPixmap, QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (QApplication, QCalendarWidget, QCheckBox,
        QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QLayout, QWidget, QVBoxLayout, QPushButton, QLabel)
import random

FPS = 60
CANVAS_WIDTH, CANVAS_HEIGHT = 400, 300
PADDING = 20
SPACE_TO_BAR_RATIO = 0.5
SWAP_FRAMES = 10
IDLE_FRAMES = 3
DEFAULT_COLOR = Qt.blue


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

class Shape(object):
    def __init__(self, points, color=DEFAULT_COLOR):
        self.points = points
        self.default_color = color
        self.color = color

    def draw(self, canvas):
        canvas.drawShape(self.points, self.color)

    def move(self, dx, dy):
        for p in self.points:
            p.x += dx
            p.y += dy

    def defaultColor(self):
        self.color = self.default_color

    def changeColor(self, color):
        self.color = color

class Bar(object):
    def __init__(self, val, ind, shape):
        self.val = val
        self.shape = shape

    def move(self, dx, dy):
        self.shape.move(dx, dy)

    def changeColor(self, color):
        color_dict = {"red": Qt.red,
            "blue": Qt.blue,
            "yellow": Qt.yellow,
            "orange": QColor('#ffa500'),
            "green": Qt.green,
            "grey": Qt.gray,
            "default": DEFAULT_COLOR}
        if type(color) == str:
            color = color_dict[color]
        self.shape.changeColor(color)

    def draw(self, canvas):
        self.shape.draw(canvas)

class Sorter:
    def selectionSort(inp_list):
        actions = []
        for i in range(len(inp_list) - 1):
            actions.append(Action("color", i, "red"))
            # find index of item with smallest value
            min_val = inp_list[i]
            min_ind = i
            last_min_ind = i
            for ind, val in enumerate(inp_list[i:], start=i):
                actions.append(Action("color", ind, "yellow"))
                if val < min_val:
                    min_ind, min_val = ind, val
                    actions.append(Action("color", ind, "orange"))
                    actions.append(Action("color", last_min_ind, "default"))
                    last_min_ind = ind
                else:
                    actions.append(Action("color", ind, "default"))
            if i == min_ind:
                actions.append(Action("color", i, "grey"))
                continue
            actions.append(Action("color", min_ind, "green"))
            # swap i-th item with next smallest item
            inp_list[i], inp_list[min_ind] = inp_list[min_ind], inp_list[i]
            actions.append(Action("swap", i, min_ind))
            actions.append(Action("color", i, "grey"))
            actions.append(Action("color", min_ind, "default"))
        return actions

class Canvas(QLabel):
    def __init__(self, width, height):
        super(Canvas, self).__init__()
        self.setPixmap(QPixmap(width, height))
        self.pixmap().fill(QColor(Qt.white))

    def clearAll(self):
        self.pixmap().fill(QColor(Qt.white))

    def drawShape(self, points, color=Qt.blue):
        qpts = [QPoint(p.x, p.y) for p in points]

        p = QPainter(self.pixmap())
        p.setPen(QPen(Qt.NoPen))
        p.setBrush(QBrush(color, Qt.SolidPattern))
        p.drawPolygon(*qpts)

class Action(object):
    def __init__(self, action_name, item1, item2):
        self.name = action_name # "color yellow", compare, swap, scan
        self.item1 = item1
        self.item2 = item2

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.item1, self.item2)

class StateTracker(object):
    def __init__(self):
        self.counter = 0
        self.state = "waiting"

    def getState(self):
        if self.state in ["done", "waiting", "next frame"]:
            return self.state
        self.counter += 1
        if self.state == "idle":
            if self.counter == IDLE_FRAMES:
                self.state = "next action"
                self.counter = 0
        elif self.state == "next action":
            self.state = "idle"
            self.counter = 0
        return self.state

    def startAnimation(self):
        self.state = "next action"

    def startSwap(self):
        self.state = "next frame"

    def endSwap(self):
        self.state = "idle"
        self.counter = 0

    def endAnimation(self):
        self.state = "done"

class ActionTracker(object):
    def __init__(self, array):
        self.counter = 0
        self.actions = self.createActions(array)

    def createActions(self, array):
        return Sorter.selectionSort(array)

    def getNextAction(self):
        try:
            next_action = self.actions[self.counter]
        except IndexError:
            return False
        self.counter += 1
        return next_action

class Swapper(object):
    def __init__(self, bar1, bar2):
        self.counter = 0
        self.bar1, self.bar2 = bar1, bar2

    def calculateFrames(self, h_swap_dist):
        h_step = h_swap_dist / SWAP_FRAMES
        self.dir_arr = [(h_step, - (SWAP_FRAMES - 1) * 5 / 2 + 5 * step) for step in range(SWAP_FRAMES)]

    def nextFrame(self):
        try:
            dx, dy = self.dir_arr[self.counter]
            self.bar1.move(dx, dy)
            self.bar2.move(-dx, -dy)
            self.counter += 1
            return True
        except IndexError:
            return False

class SortVisualizer(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.state_tracker = StateTracker()

        array = [random.randint(1, 101) for _ in range(15)]
        self.createBars(array)
        self.action_tracker = ActionTracker(array)

    def createBars(self, array):
        self.bars = []
        space_from_bottom = 50
        max_val = max(array)
        arr_len = len(array)
        v_unit = (CANVAS_HEIGHT - 2 * PADDING - space_from_bottom) / max_val
        self.h_unit = (CANVAS_WIDTH - 2 * PADDING) / (arr_len * (1 + SPACE_TO_BAR_RATIO) - 0.5)
        self.spacing_btw_bars = self.h_unit * SPACE_TO_BAR_RATIO
        
        y2 = CANVAS_HEIGHT - PADDING - space_from_bottom
        for index, val in enumerate(array):
            x1 = PADDING + index * (self.spacing_btw_bars + self.h_unit)
            x2 = PADDING + index * (self.spacing_btw_bars + self.h_unit) + self.h_unit
            y1 = y2 - v_unit * val
            shape = Shape([
                Point(x1, y1),
                Point(x2, y1),
                Point(x2, y2),
                Point(x1, y2)])
            self.bars.append(Bar(val, index, shape))

    def update(self):
        state = self.state_tracker.getState()
        if state == "done":
            return
        elif state == "next action":
            self.curr_action = self.action_tracker.getNextAction()
            if not self.curr_action:
                self.state_tracker.endAnimation()
            elif self.curr_action.name == "swap":
                i, j = self.curr_action.item1, self.curr_action.item2
                self.swapper = Swapper(self.bars[i], self.bars[j])
                h_swap_dist = (j - i) * (self.h_unit + self.spacing_btw_bars)
                self.swapper.calculateFrames(h_swap_dist)
                self.state_tracker.startSwap()

            elif self.curr_action.name == "color":
                # change color of bar to specified color
                index = self.curr_action.item1
                color = self.curr_action.item2
                print("index: {}, color: {}".format(index, color))
                self.bars[index].changeColor(color)
        elif state == "next frame": # do next frame of swap
            if not self.swapper.nextFrame():
                # end of swap
                i, j = self.curr_action.item1, self.curr_action.item2
                self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
                self.state_tracker.endSwap()

        
    def draw(self):
        for bar in self.bars:
            bar.draw(self.canvas)

    def buttonPressed(self):
        print("button pressed")
        self.state_tracker.startAnimation()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createGeneralOptionsGroupBox()
        self.createCanvasGroupBox()

        self.setupLayout()
        self.show()
        self.setup()

    def setupLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0)
        layout.addWidget(self.generalOptionsGroupBox, 0, 1)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

    def createGeneralOptionsGroupBox(self):
        self.generalOptionsGroupBox = QGroupBox("General Options")

        self.selectionModeCombo = QComboBox()
        self.selectionModeCombo.addItem("Single selection",
                QCalendarWidget.SingleSelection)
        self.selectionModeCombo.addItem("None",
                QCalendarWidget.NoSelection)
        self.selectionModeLabel = QLabel("&Selection mode:")
        self.selectionModeLabel.setBuddy(self.selectionModeCombo)

        pushButton = QPushButton("&Normal Button")
        pushButton.clicked.connect(self.pushButtonPressed)

        outerLayout = QGridLayout()
        outerLayout.addWidget(pushButton, 0, 0)
        outerLayout.addWidget(self.selectionModeLabel, 1, 0)
        outerLayout.addWidget(self.selectionModeCombo, 1, 1)
        self.generalOptionsGroupBox.setLayout(outerLayout)

    def pushButtonPressed(self):
        self.sort_visualizer.buttonPressed()

    def createCanvasGroupBox(self):
        self.canvasGroupBox = QGroupBox("Canvas")
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.canvasLayout = QGridLayout()
        self.canvasLayout.addWidget(self.canvas, 0, 0, Qt.AlignCenter)
        self.canvasGroupBox.setLayout(self.canvasLayout)

    def setup(self):
        # insert initial conditions for animation
        self.sort_visualizer = SortVisualizer(self.canvas)

        self.timer = QTimer()
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000 // FPS)
    
    def mainloop(self):
        self.canvas.clearAll()
        self.update()
        self.canvas.update()

    def update(self):
        # code that executes between frames for animation
        self.sort_visualizer.update()
        self.sort_visualizer.draw()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())