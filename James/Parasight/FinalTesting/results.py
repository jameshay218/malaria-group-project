import base64
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import base64
import thread

class Results(QtGui.QDialog):
    emitCloseResults = QtCore.pyqtSignal()
    def __init__(self, givenResults, answers, testCount, error, remainingTime):
        super(Results, self).__init__()
        self.styleData = ''
        
        f = open('style', 'r')
        self.styleData = f.read()
        f.close()
        self.resultsUI(givenResults, answers, testCount, error, remainingTime)
        
    def resultsUI(self, givenResults, answers, testCount, error, remainingTime):
        marks = 0
        maxMarks = len(answers)
        percentage = 0
        if testCount == True:
            maxMarks *= 3
        else:
            maxMarks *= 2
        
        #Create grid layout
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        #Font for title
        titleFont = QtGui.QFont()
        titleFont.setPointSize(12)
        titleFont.setBold(True)
        superTitleFont = QtGui.QFont()
        superTitleFont.setPointSize(22)
        superTitleFont.setBold(True)

        #heading = QLabel('Results')
        #heading.setFont(superTitleFont)
        titleLabel = QLabel(self)
        self.bannerImage = QtGui.QPixmap('images/ResultsTrans.png')
        self.bannerImageScaled = self.bannerImage.scaled(250, 60, Qt.KeepAspectRatio)
        titleLabel.setPixmap(self.bannerImageScaled)
        self.grid.addWidget(titleLabel, 0, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.tableResults = QTableWidget()
        self.tableResults.setRowCount(len(answers)+1)
        self.tableResults.setColumnCount(9)
        
        self.tableResults.setItem(0, 0, QTableWidgetItem('Question'))
        self.tableResults.setItem(0, 1, QTableWidgetItem('Given Diagnosis'))
        self.tableResults.setItem(0, 2, QTableWidgetItem('Actual Diagnosis'))
        self.tableResults.setItem(0, 3, QTableWidgetItem('Given Strain'))
        self.tableResults.setItem(0, 4, QTableWidgetItem('Actual Strain'))
        self.tableResults.setItem(0, 5, QTableWidgetItem('Given Count'))
        self.tableResults.setItem(0, 6, QTableWidgetItem('Actual Count'))
        self.tableResults.setItem(0, 7, QTableWidgetItem('Correct?'))
        self.tableResults.setItem(0, 8, QTableWidgetItem('Accuracy'))
        
        headerFont = QFont()
        headerFont.setBold(True)
        for j in range(0, 9):
            self.tableResults.item(0, j).setFont(headerFont)

        for i in range(1, len(answers)+1):
            adding = str(i)
            self.tableResults.setItem(i, 0, QTableWidgetItem(adding))
            self.tableResults.setItem(i, 1, QTableWidgetItem(givenResults[i-1][0]))
            self.tableResults.setItem(i, 2, QTableWidgetItem(answers[i-1][0]))
                                      
            self.tableResults.setItem(i, 3, QTableWidgetItem(givenResults[i-1][1]))
            self.tableResults.setItem(i, 4, QTableWidgetItem(answers[i-1][1]))                        
                    
            if testCount == True:
                self.tableResults.setItem(i, 5, QTableWidgetItem(str(givenResults[i-1][2])))
            else:
                self.tableResults.setItem(i, 5, QTableWidgetItem('N/A'))
            self.tableResults.setItem(i, 6, QTableWidgetItem(str(answers[i-1][2])))

            if str(givenResults[i-1][0]) == str(answers[i-1][0]):
                marks += 1
            if str(givenResults[i-1][1]) == str(answers[i-1][1]):
                marks += 1 

            if str(givenResults[i-1][0]) == str(answers[i-1][0]) and str(givenResults[i-1][1]) == str(answers[i-1][1]):
                if testCount == True:
                    if float(answers[i-1][2]) <= (givenResults[i-1][2] + (givenResults[i-1][2] * error)) and float(answers[i-1][2]) >= (givenResults[i-1][2] - (givenResults[i-1][2] * error)):
                        marks += 1
                        self.tableResults.setItem(i, 7, QTableWidgetItem('Correct'))
                        self.tableResults.item(i, 7).setBackground(QtGui.QColor(13, 255, 95))
                    else:
                        self.tableResults.setItem(i, 7, QTableWidgetItem('Incorrect'))
                        self.tableResults.item(i, 7).setBackground(QtGui.QColor(231, 76, 60))
                else:
                    self.tableResults.setItem(i, 7, QTableWidgetItem('Correct'))
                    self.tableResults.item(i, 7).setBackground(QtGui.QColor(13, 255, 95))
            else:
                self.tableResults.setItem(i, 7, QTableWidgetItem('Incorrect'))
                self.tableResults.item(i, 7).setBackground(QtGui.QColor(231, 76, 60))
            if testCount == True:
                if answers[i-1][2] != 0:
                    self.tableResults.setItem(i, 8, QTableWidgetItem(str(1-(abs(givenResults[i-1][2] - answers[i-1][2])/answers[i-1][2]))))
                elif answers[i-1][2] == 0 and givenResults[i-1][2] == 0:
                    self.tableResults.setItem(i, 8, QTableWidgetItem('1.0'))
                else:
                    self.tableResults.setItem(i, 8, QTableWidgetItem('0.0'))
            else:
                self.tableResults.setItem(i, 8, QTableWidgetItem('N/A'))

        header = self.tableResults.horizontalHeader()
        header.setStretchLastSection(True)
        self.tableResults.verticalHeader().setVisible(False)
        #self.tableResults.horizontalHeader().setVisible(False)
        self.tableResults.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.grid.addWidget(self.tableResults, 1, 0, 1, 2)
                                      
          
        percentage = (float(marks)/float(maxMarks)) * 100.0
        percentageResult = 'Percentage: ' + `percentage` + '%'
        percentageLabel = QLabel(percentageResult)
        percentageLabel.setFont(superTitleFont)
        percentageLabel.setStyleSheet('font-size: 16px')
        self.grid.addWidget(percentageLabel, 2, 0, 1, 1, QtCore.Qt.AlignCenter)
        
        takenMinutes = int(remainingTime/60)
        takenSeconds = int(remainingTime%60)
        
        timeTaken = str('{:02}'.format(takenMinutes)) + ':' + str('{:02}'.format(takenSeconds))
        timeResult = 'Time taken: ' + timeTaken
        timeTakenLabel = QLabel(timeResult)
        timeTakenLabel.setFont(superTitleFont)
        timeTakenLabel.setStyleSheet('font-size: 16px')
        #timerLabel.setFont(titleFont)
        #self.grid.addWidget(timerLabel, rowNumber, 1, 1, 1, QtCore.Qt.AlignCenter)
        self.grid.addWidget(timeTakenLabel, 2, 1, 1, 1, QtCore.Qt.AlignCenter)
        

        closeButton = createButton('Close', self.closeWindow, 'Close the results page')
        self.grid.addWidget(closeButton, 4, 0, 1, 2, QtCore.Qt.AlignCenter)
        
        
        #Final window housekeeping
        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Results') #Title of the program
        self.setWindowIcon(QIcon('images/logo.png'))
        self.setFixedSize(1000, 700)
        #self.resize(600, 600)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.emitCloseResults.emit()  
            self.close()

    def closeEvent(self, event):
        self.emitCloseResults.emit()  
        event.accept()

    def closeWindow(self):
        self.emitCloseResults.emit()
        self.close()

def createButton(name, buttonFunction, tooltip):
    btn = QPushButton(name)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip(tooltip)
    return btn
