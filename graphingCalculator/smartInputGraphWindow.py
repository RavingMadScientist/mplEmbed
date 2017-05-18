# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:47:21 2016

@author: legitz7
"""

from PyQt4 import QtCore, QtGui, Qt
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backend_bases import key_press_handler
import math
import numpy as np




def startsWith(longString, subString):
    compLength = len(subString)
    if compLength > len(longString):
        return False
    if longString[:compLength] == subString:
        return True
    else:
        return False

def endsWith(longString, subString):
    compLength = len(subString)
    if compLength > len(longString):
        return False
    if longString[-1*compLength:] == subString:
        return True
    else:
        return False


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)        
        self.initUI()
    def initUI(self):
        self.main_frame = QtGui.QWidget()        
        self.setWindowTitle("Basic mpl/PyQt Graphing Calculator")
        
# Entry widgets and logic        
        self.funcLabel = QtGui.QLabel("y(x) = ")
        self.funcEntry = QtGui.QLineEdit("Type your function here")
        self.funcEntry.setCursorPosition(0)

        self.rangeLoLabel = QtGui.QLabel("From: ")
        self.rangeLoEntry = QtGui.QLineEdit("0.0")
        self.rangeLoEntry.setCursorPosition(0)

        self.rangeHiLabel = QtGui.QLabel(" To: ")
        self.rangeHiEntry = QtGui.QLineEdit("1.0")
        self.rangeHiEntry.setCursorPosition(0)

        self.numSampsLabel = QtGui.QLabel("#Points = ")
        self.numSampsEntry = QtGui.QLineEdit("200")     
        
        self.sampSpaceLabel = QtGui.QLabel("Step Size: ")
        self.sampSpaceEntry = QtGui.QLineEdit("")

        self.goButton = QtGui.QPushButton("Display!")
        self.goButton.clicked.connect(self.makeGraph)

#Output-display widgets and logic        
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


#Layout logic

        leftBox = QtGui.QGridLayout()
        leftBox.setHorizontalSpacing(10)
        #self.pushLabel = QtGui.QSpacerItem(200,200)
        leftBox.addWidget(self.funcLabel, 0, 0,1 ,1)
        leftBox.addWidget(self.funcEntry, 0, 1, 1, 3)
        #leftBox.addItem(self.pushLabel, 0,4,3,4)
        leftBox.addWidget(self.rangeLoLabel, 1, 0,1,1)
        leftBox.addWidget(self.rangeLoEntry, 1, 1,1,1)
        leftBox.addWidget(self.rangeHiLabel, 1, 2,1,1)
        leftBox.addWidget(self.rangeHiEntry, 1, 3,1,1)
        leftBox.addWidget(self.numSampsLabel, 2, 0,1,1)
        leftBox.addWidget(self.numSampsEntry, 2, 1,1,1)
        leftBox.addWidget(self.sampSpaceLabel, 3, 0,1,1)
        leftBox.addWidget(self.sampSpaceEntry, 3, 1,1,1)
        leftBox.addWidget(self.goButton, 4, 0,1,1)

        self.dumbWidget = QtGui.QWidget()
        self.dumbWidget.setFixedWidth(300)
        self.dumbWidget.setLayout(leftBox)
        
        rightBox = QtGui.QVBoxLayout()
        rightBox.addWidget(self.canvas)  # the matplotlib canvas
        rightBox.addWidget(self.ntb)
        
        leftRight = QtGui.QHBoxLayout()
        leftRight.addWidget(self.dumbWidget)
        leftRight.addLayout(rightBox)
        self.main_frame.setLayout(leftRight)
        self.setCentralWidget(self.main_frame)

    def on_key_press(self, event):
        print('you pressed', event.key)
        key_press_handler(event, self.canvas, self.ntb)
        
        
    """
    Overview of the method: responds to clicks of the 'Display!' button
    1) validates the string in self.funcEntry
    2) validates the Lo, Hi, and Samps Entries
    3) attempts to eval the string within a for-loop over the range defined by domain specs
    
    """
    def makeGraph(self):
#begin validation
        ValidEval = True
        errorFound = ""
        okLibs=["math"]
        okParams=['key']
        badWords=[" break", " class", " def", " del", " eval", " exec", " global", " import", " open"]
        rawStatement=str(self.funcEntry.text()).strip()
        
        if len(rawStatement) == 0:
            ValidEval = False
            errorFound="no Entry"
        for epos, echar in enumerate(rawStatement):
            if echar=='.' and epos > 0:
                checkchar=rawStatement[epos-1]
                if checkchar.isalpha():
                    libVerified = False
                    checkThis = rawStatement[:epos].split(' ')[-1]
                    for eLib in okLibs:
                        checkLib = endsWith(checkThis, eLib)
                        if checkLib:
                            libVerified = True
                        
                    if not libVerified:
                        ValidEval = False
                        errorFound="Illegal Library request: "+ checkThis

            if echar=='=':
                if (epos == 0 or (epos==len(rawStatement)-1)):
                    ValidEval = False
                    errorFound = "Bad Syntax, can't use peripheral '='"
                else:    
                    checkchar = rawStatement[epos-1]
                    if not (  (checkchar=='>') or (checkchar=='<') or (checkchar=='!') or (checkchar=='=') or rawStatement[epos+1]=='='):
                        checkThis = rawStatement[:epos].strip(' ')
                        paramVerified = False
                        for eParam in okParams:
                            checkParam = endsWith(checkThis, eParam)
                            if checkParam:
                                paramVerified = True
                        if not paramVerified:
                            ValidEval = False
                            errorFound = "Illegal assignment operator"
        for badWord in badWords:
            if badWord in rawStatement or startsWith(rawStatement, badWord[1:]):
                ValidEval = False
                errorFound = "Illegal phrase used: " + badWord + " --watch yourself!"


        #OK now we can try to scrape the parameters...
        numType = 'int'
        if ValidEval:
            boundKeys = ["rangeLo", "rangeHi", "numSamples", "sampleSpacing"]
            boundWidgets=[self.rangeLoEntry, self.rangeHiEntry, self.numSampsEntry, self.sampSpaceEntry]
            self.boundDict = {}
            
            numStrikes = 0
            maxStrikes = 2
            numVerified = 0
            maxVerified = 3
            for epos, ewidget in enumerate(boundWidgets):
                rawVal = str(ewidget.text()).strip()
                try:
                    rawInt = int(rawVal)
                    self.boundDict[boundKeys[epos]] = rawInt
                    numVerified += 1
                except:
                    try:
                        rawFloat = float(rawVal)
                        self.boundDict[boundKeys[epos]] = rawFloat
                        numVerified += 1
                        numType = 'float'
                    except:
                        numStrikes += 1
                        if epos == 0 or numStrikes >= maxStrikes:
                            ValidEval = False
                            errorFound = "Too Many illegal boundary conditions"
                if numVerified >= maxVerified:
                    break

        if ValidEval and not errorFound:
            print "ValidEval for entry:"
            print rawStatement    
            print "boundDict: "
            print self.boundDict
            try:
                
                if "sampleSpacing" in self.boundDict.keys():
                    if "rangeHi" in self.boundDict.keys():
                        self.x = np.arange(self.boundDict['rangeLo'], self.boundDict['rangeHi'], self.boundDict['sampleSpacing'], dtype = numType)
                    elif "numSamples" in self.boundDict.keys():
                        self.x = np.full((self.boundDict['numSamples'],), self.boundDict['rangeLo'], dtype = numType)
                        
                        stepSize = self.boundDict['sampleSpacing']                        
                        for i in range(1,self.x.size):
                            self.x[i] = self.x[i-1] + stepSize
                    else:
                        raise LookupError
                            
                elif "rangeHi" in self.boundDict.keys() and "numSamples" in self.boundDict.keys():
                    self.x = np.linspace(self.boundDict['rangeLo'], self.boundDict['rangeHi'], self.boundDict['numSamples'])
                else:
                    raise LookupError
                
                self.y = np.zeros((self.x.size,))
                goodEvals = 0
                print 'initial config ok'
                for ePos, eVal in enumerate(self.x):
                    try:
                        x=eVal
                        self.y[ePos]=eval(rawStatement)
                        goodEvals += 1
                    except:
                        self.y[ePos] = np.nan
                        #Function has to evaluate correctly for the lower bound, 
                        #in order to guard against wasting massive cycles on a syntax error
                        if ePos == 0:
                            print "first eval fails. breaking loop"
                            break
                
                if goodEvals >= 1:
                    print("good Evaluation: "+ str(goodEvals) )
                    self.axes.cla()
                    self.axes.plot(self.x, self.y)                
                    self.canvas.draw()
                else:
                    errorFound = "unconclusive eval statement. check your syntax" 
            except:
                errorFound = "execution error"
                print errorFound
        else:
            print "entry Error:"
            print errorFound
        if errorFound:
            print "generating QMessageBox"
            errorString ='"Cause every little thing; is gonna be alright"... someday. But not today, sorry. \nPlease try a better function.\n Immune response rejection status(es):\n' + errorFound  
            ermg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, 'No bueno!', errorString)
            ermg.exec_()
            
            
 

        
def main():

    qApp = QtGui.QApplication(sys.argv)
    a=ApplicationWindow()
    a.show()
    sys.exit(qApp.exec_())
if __name__ == '__main__':
    main() 