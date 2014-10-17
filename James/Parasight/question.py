import base64
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import base64
import thread
import time
from time import strftime


# QDialog class to display an image and allow user to choose accompanying labels
class myQuestion(QtGui.QDialog):
    imageIndex = 0
    imageHeight = 16
    imageWidth = 21
    givenAnswers = []
    # Properties to monitor quiz time out and submission of quiz answers
    emitResults = QtCore.pyqtSignal(object)
    timeOut = QtCore.pyqtSignal()
    
    def __init__(self, useCount, criteria, answers, error, startingTimeSeconds, startingTimeMinutes):
        super(myQuestion, self).__init__()
        self.styleData = ''
         
        # Set the window style
        f = open('style', 'r')
        self.styleData = f.read()
        f.close()

        # Set the optional properties of the quiz (time, test on count or not etc)
        self.imageResults = answers
        self.testCount = useCount
        self.possibleAnswers = ['']
        self.maxMinutes = startingTimeMinutes
        self.maxSeconds = startingTimeSeconds
        self.maxTime = startingTimeSeconds + (60*startingTimeMinutes)

        for criterion in criteria:
            self.possibleAnswers.append(criterion)
        
        #Set list of answers to empty
        self.givenAnswers = []
        for answer in answers:
            self.givenAnswers.append(['', '', 0.0])
            
        self.initQuestionUI()

    def initQuestionUI(self):
        #Create grid layout
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
       
        
        #Font for title
        titleFont = QtGui.QFont()
        titleFont.setPointSize(12)
        titleFont.setBold(True)
        self.questionNumber = QLabel('Question 1')
        self.questionNumber.setFont(titleFont)
        self.grid.addWidget(self.questionNumber, 0, 0, 1, self.imageWidth + 3, QtCore.Qt.AlignCenter)
        
        #Timer
        timerLabel = QLabel('Time Remaining:')
        #self.grid.addWidget(timerLabel, 1, 0, 1, 4, QtCore.Qt.AlignLeft)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.lcd.display(str('{:02}'.format(self.maxMinutes)) + ':' + str('{:02}'.format(self.maxSeconds)))
        self.grid.addWidget(self.lcd, 2, self.imageWidth, 1, 3, QtCore.Qt.AlignCenter)

        #First image
        self.currentImage = self.displayImage(self.imageResults[self.imageIndex][3])
        self.grid.addWidget(self.currentImage, 2, 0, self.imageHeight, self.imageWidth)

        #Answer options
        heading = QLabel('Answers:')
        heading.setFont(titleFont)
        self.grid.addWidget(heading, 3, self.imageWidth, 1, 3, QtCore.Qt.AlignCenter)
        self.diagnosis = QComboBox()
        self.diagnosis.addItem('')
        self.diagnosis.addItem('positive')
        self.diagnosis.addItem('negative')
        self.grid.addWidget(self.diagnosis, 4, self.imageWidth, 1, 3)

        self.strain = QComboBox()
        for option in self.possibleAnswers:
            self.strain.addItem(option)
        self.grid.addWidget(self.strain, 5, self.imageWidth, 1, 3)

        self.count = QDoubleSpinBox()
        self.count.setRange(0, 1)
        self.count.setDecimals(3)
        self.count.setSingleStep(0.001)
        rowCount = 6
        if self.testCount == True:
            self.grid.addWidget(self.count, rowCount, self.imageWidth, 1, 2)
            rowCount += 1

        #Image movement buttons
        nextButton = createButton('Next', self.updateImageRight, 'Go to the next question')
        previousButton = createButton('Previous', self.updateImageLeft, 'Go to the previous question')
        submitButton = createButton('Submit', self.submitResults, 'Ends the quiz with your current answers')
        self.grid.addWidget(previousButton, rowCount, self.imageWidth, 1, 1)
        self.grid.addWidget(submitButton, rowCount, self.imageWidth+1, 1, 1)
        self.grid.addWidget(nextButton, rowCount, self.imageWidth+2, 1, 1)
        self.startTime = time.time()
        self.timer.start(1000)

        #Final window housekeeping
        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Active Quiz') #Title of the program
        self.setWindowIcon(QIcon('images/logo.png'))
        #self.setFixedSize(600, 600)
        self.setMaximumSize(1200, 1000)
        self.setMinimumSize(1000, 700)
        self.resize(1000, 700)
        self.show() 

    # Function to handle the countdown timer of the quiz
    def Time(self):
        # Work out elapsed time and time remaining
        elapsedTime = time.time() - self.startTime
        remainingTime = self.maxTime - elapsedTime
        
        remainingMinutes = int(remainingTime/60)
        remainingSeconds = int(remainingTime%60)
        showElapsedTime = str('{:02}'.format(remainingMinutes)) + ':' + str('{:02}'.format(remainingSeconds))
        
        if int(remainingTime) == 0:
            self.forceSubmit()

        # Update the timer with the remaining time
        self.lcd.display(showElapsedTime)
                             
    # Changes the displayed image and answers to that saved in the index to the right of the 
    # current result
    def updateImageRight(self):
        self.updateAnswers()
        if self.imageIndex == len(self.imageResults) - 1:
            self.imageIndex = 0
        else:
            self.imageIndex += 1
        self.changeCurrentImage(self.imageResults[self.imageIndex][3])
        question = "Question " + `self.imageIndex + 1`
        self.questionNumber.setText(question)
        self.setAnswerState()
                          
    # Changes the displayed image and answers to that saved in the index to the left of the 
    # current result
    def updateImageLeft(self):
        self.updateAnswers()
        if self.imageIndex == 0:
            self.imageIndex = len(self.imageResults) - 1
        else:
            self.imageIndex -= 1
        self.changeCurrentImage(self.imageResults[self.imageIndex][3])
        question = "Question " + `self.imageIndex + 1`
        self.questionNumber.setText(question)
        self.setAnswerState()

    # Creates an image from the given byte array and returns it as a QLabel to be added to the
    # window
    def displayImage(self, byte_array):
        image_bytes = base64.b64decode(byte_array)
        label = QtGui.QLabel(self)
        qimg = QtGui.QPixmap()
        qimg.loadFromData(image_bytes)
        #qimgScaled = qimg.scaled(300, 300)
        label.setPixmap(qimg)
        label.setScaledContents(False)
        label.setAlignment(Qt.AlignTop)
        return label

    # Changes the currently displayed image to that from the given byte array
    def changeCurrentImage(self, byte_array):
        image_bytes = base64.b64decode(byte_array)
        qimg = QtGui.QPixmap()
        qimg.loadFromData(image_bytes)
        self.currentImage.setPixmap(qimg)
        self.resize(self.sizeHint())
        
    # Changes the displayed answers to match those corresponding to the current answer index
    def updateAnswers(self):
        self.givenAnswers[self.imageIndex][0] = str(self.diagnosis.currentText())
        self.givenAnswers[self.imageIndex][1] = str(self.strain.currentText())
        self.givenAnswers[self.imageIndex][2] = self.count.value()
        return

    def setAnswerState(self):
        #Update diagnosis dropdown
        index = 0
        if self.givenAnswers[self.imageIndex][0] == 'positive':
            index = 1
        elif self.givenAnswers[self.imageIndex][0] == 'negative':
            index = 2
        self.diagnosis.setCurrentIndex(index)

        #Update strain dropdown
        index = 0
        for i in range(0, len(self.possibleAnswers)):
            if self.givenAnswers[self.imageIndex][1] == self.possibleAnswers[i]:
                index = i
                break
        self.strain.setCurrentIndex(index)

        #Set count
        self.count.setValue(self.givenAnswers[self.imageIndex][2])
        return

    # Checks that the user is ready to submit their answers, and if so, saves the remaining time
    # and given answers. Saves these as a tuble and signals to the results class that the quiz is
    # completed ready to calculate results
    def submitResults(self):
        self.updateAnswers()
        reply = QtGui.QMessageBox.question(self, 'Warning!', \
            "Are you sure that you are finished?", \
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return
        #print self.givenAnswers
        elapsedTime = time.time() - self.startTime
        remainingTime = int(self.maxTime - elapsedTime)
        allAnswers = self.givenAnswers
        self.givenAnswers = []
        toReturn = (allAnswers, remainingTime)
        self.emitResults.emit(toReturn)
        self.close()
        
    def forceSubmit(self):
        self.updateAnswers()
        elapsedTime = time.time() - self.startTime
        remainingTime = int(self.maxTime - elapsedTime)
        toReturn = (self.givenAnswers, remainingTime)
        self.emitResults.emit(toReturn)
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.submitResults()

# Helper function to create a push button with a given name, function and tooltip
def createButton(name, buttonFunction, tooltip):
    btn = QPushButton(name)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip(tooltip)
    return btn
