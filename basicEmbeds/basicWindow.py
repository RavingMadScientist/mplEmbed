# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:44:31 2016

@author: legitz7
"""
"""
This is the first example from the tutorial at ravingmadscientist.org/code/Tutorials/mplPyQt_001.html
It is not especially useful
"""
from PyQt4 import QtCore, QtGui, Qt
import sys
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)        
        self.initUI()
    def initUI(self):
        self.main_frame = QtGui.QWidget()        
        self.setWindowTitle("Matplotlib Figure in a Qt4 Window")
        self.fig=Figure() 
        self.axes = self.fig.add_subplot(111)
        self.x = np.arange(0.0, 1.0, 0.01)
        self.y = np.cos(2*np.pi*self.x + 5) + 2
        self.axes.plot(self.x, self.y)
        self.canvas=FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
def main():
    qApp = QtGui.QApplication(sys.argv)
    a=ApplicationWindow()
    a.show()
    sys.exit(qApp.exec_())
if __name__ == '__main__':
    main() 