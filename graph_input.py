import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from grapher import *

class EquationApp(QWidget):
    my_clicked = pyqtSignal(str,str,str,str)
    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle('Graphing Calculator')
        self.setFixedSize(width, height)
        self.createWidgets()
        self.arrangeWidgets()
        self.makeConnections()

    def createWidgets(self):
        self.equation_label = QLabel("Equation of graph y = f(x)")
        self.equation_input = QLineEdit()
        self.polar_label = QLabel("Equation of graph r = g(θ)")
        self.polar_input = QLineEdit()
        self.para_label = QLabel("Parametric equation of graph x = f(t) y = f(t)")
        self.para_input1 = QLineEdit()
        self.para_input2 = QLineEdit()
        self.draw_btn = QPushButton("Draw!")

    def arrangeWidgets(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(self.equation_label)
        row1.addWidget(self.equation_input)
        
        row2 = QHBoxLayout()
        row2.addWidget(self.polar_label)
        row2.addWidget(self.polar_input)

        row3 = QVBoxLayout()  
        row3.addWidget(self.para_label)
        row3a = QHBoxLayout()
        row3a.addWidget(self.para_input1)
        row3a.addWidget(self.para_input2)
        row3.addLayout(row3a)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addWidget(self.draw_btn, Qt.AlignCenter)
        layout.addStretch(1)
        self.setLayout(layout)

    def click(self):
        self.my_clicked.emit(self.equation_input.text(), self.polar_input.text(), self.para_input1.text(), self.para_input2.text())

    def makeConnections(self):
        self.draw_btn.clicked.connect(self.click)

class PlotCanvas(FigureCanvas):

    def __init__(self, xwidth, yheight, parent=None, width=5, height=4, dpi=100):
        self.xwidth = xwidth
        self.yheight = yheight
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.plot([])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, coords_from_eqs):
        self.axes.clear()
        for coords in coords_from_eqs:
            self.axes.plot(coords, 'r-')
        self.axes.set_title("plot")
        self.axes.figure.canvas.draw()

    def click_get_coords(self, e1, e2, e3a, e3b):
        coords = generateCoordinates(e1, e2, e3a, e3b, self.xwidth, self.yheight)
        self.plot(coords)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    width, height = 400, 250
    input_window = EquationApp(width,height)
    canvas_window = PlotCanvas(width, height)

    input_window.my_clicked.connect(canvas_window.click_get_coords)
    input_window.my_clicked.connect(canvas_window.show)

    input_window.show()

    sys.exit(app.exec_())