# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:47:21 2016

@author: legitz7
"""
"""
This is the second tutorial example from http://ravingmadscientist.org/code/Tutorials/mplPyQt_001.html
The mpl Navigation Toolbar is included with a mpl Figure as a compound PyQt4 widget, displaying a 
hardcoded 1:1  Numpy function
"""
from PyQt4 import QtCore, QtGui, Qt
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backend_bases import key_press_handler
import numpy as np

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)        
        self.initUI()
    def initUI(self):
        self.main_frame = QtGui.QWidget()        
        self.setWindowTitle("Matplotlib Figure in a Qt4 Window with Navigation Toolbar")
        self.fig=Figure() 
        self.axes = self.fig.add_subplot(111)
        self.x = np.arange(0.0, 1.0, 0.01)
        self.y = np.cos(2*np.pi*self.x + 5) + 2
        self.axes.plot(self.x, self.y)
        self.canvas=FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()
        self.ntb = NavigationToolbar(self.canvas, self.main_frame)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
       
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.ntb)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def on_key_press(self, event):
        print('you pressed', event.key)
        key_press_handler(event, self.canvas, self.ntb)
 
        
def main():

    qApp = QtGui.QApplication(sys.argv)
    a=ApplicationWindow()
    a.show()
    sys.exit(qApp.exec_())
if __name__ == '__main__':
    main() 