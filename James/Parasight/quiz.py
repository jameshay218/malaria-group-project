import sys
#Package containing all list options
from PyQt4 import QtGui, QtCore
from lists import *
from results import *
from database import *
from question import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import base64
import thread

class Quiz(QtGui.QDialog):
    answers = []
    parasiteCriteria = []
    timer = 0
    allResults = []
    newQuiz = None
    emitClose = QtCore.pyqtSignal()
    timeAllowed = 0

    def __init__(self):
        super(Quiz, self).__init__()
        #self.setStyleSheet('font-size: 11pt; font-family: Arial;')
        self.styleData = ''
        
        f = open('style', 'r')
        self.styleData = f.read()
        f.close()
        self.quizUI()
        
    def quizUI(self):
        #Create grid layout
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(8)
        
        
        #Set up title and add to grid
        titleLabel = QLabel(self)
        self.bannerImage = QtGui.QPixmap('images/DiagnosisQuizTrans.png')
        self.bannerImageScaled = self.bannerImage.scaled(250, 60, Qt.KeepAspectRatio)
        titleLabel.setPixmap(self.bannerImageScaled)
        self.grid.addWidget(titleLabel, 0, 0, 1, 10, QtCore.Qt.AlignCenter)
        
        #Take description from list file and add to grid
        quizDescription = QLabel(QUIZ_DESCRIPTION)
        quizDescription.setWordWrap(True)
        self.grid.addWidget(quizDescription, 1, 0, 5, 10, Qt.AlignTop | Qt.AlignJustify)
        
        #Add spin box for number of questions
        questionsLabel = QLabel('Number of images:')
        self.noQuestions = QSpinBox()
        self.noQuestions.setRange(1, 99)
        self.noQuestions.setValue(10)
        self.grid.addWidget(questionsLabel, 10, 2, 1, 2)
        self.grid.addWidget(self.noQuestions, 10, 4, 1, 2)

        #Add dropdown for parasite strains
        speciesLabel = QLabel('Species to be tested:')
        self.speciesOptions = QComboBox(self)
        speciesAdd = createButton('Add', self.addItem, 'Click to add parasite strain to quiz')
        for i in range(1, len(STRAIN_LIST)):
            self.speciesOptions.addItem(STRAIN_LIST[i])
        self.grid.addWidget(speciesLabel, 11, 2, 1, 2)
        self.grid.addWidget(self.speciesOptions, 11, 4, 1, 2)
        self.grid.addWidget(speciesAdd, 11, 6, 1, 2)

        #Add spin box for quiz timer
        self.minutes = QSpinBox()
        self.minutes.setRange(0, 99)
        self.minutes.setValue(5)
        self.seconds = QSpinBox()
        self.seconds.setRange(0, 59)
        self.seconds.setValue(0)
        timeLabel = QLabel('Time (mins/secs):')
        self.grid.addWidget(timeLabel, 12, 2, 1, 2)
        self.grid.addWidget(self.minutes, 12, 4, 1, 2)
        self.grid.addWidget(self.seconds, 12, 6, 1, 2)

        blank = QLabel('')
        self.grid.addWidget(blank, 13, 2, 1, 1, Qt.AlignCenter)
        
        #Checkbox to choose count
        self.includeCount = QCheckBox('Test on parasitic count (optional)')
        self.grid.addWidget(self.includeCount, 15, 2, 1, 4)

        #Allow user to set margin of error
        errorLabel = QLabel('Allowable error:')
        self.error = QDoubleSpinBox()
        self.error.setRange(0, 0.99)
        self.error.setDecimals(2)
        self.error.setSingleStep(0.01)
        self.error.setValue(0.05)
        self.grid.addWidget(errorLabel, 16, 2, 2, 2, Qt.AlignTop)
        self.grid.addWidget(self.error, 16, 4, 2, 2, Qt.AlignTop)
        
        initiateQuiz = createButton('Go!', self.startQuiz, 'Starts the quiz!')
        resetAllFields = createButton('Reset', self.resetFields, 'Resets all optional fields to default values')
        self.grid.addWidget(blank, 18, 2, 1, 8)
        self.grid.addWidget(initiateQuiz, 18, 1, 1, 4)
        self.grid.addWidget(resetAllFields, 18, 5, 1, 4)
        

        #Final window housekeeping
        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Parasight Quality Checker') #Title of the program
        self.setWindowIcon(QIcon('images/logo.png'))
        self.setFixedSize(600, 450)
        #self.resize(1000, 800)
        self.show() 
        
    # Adds the currently selected species name to the list of testable species.
    def addItem(self):
        toBeAdded = self.speciesOptions.currentText()
        if toBeAdded not in self.parasiteCriteria:
            self.parasiteCriteria.append(str(toBeAdded))
        return
                  
    # Checks that at least one strain has been specified and that a quiz is not already running.
    # If not, connects to the database and submits a query to return the specified number of
    # random images. Once the query returns, displays a warning box for the user to iniate
    # the quiz at their leisure. Once accepted, creates an instance of the question class and 
    # initiates the quiz.
    def startQuiz(self):
        if self.newQuiz is not None:
            QMessageBox.warning(self, "Attention", "A quiz is already in progress!", QMessageBox.Ok)
            return False
        databaseConnection = Database()
        if self.parasiteCriteria == []:
            QMessageBox.warning(self, "Attention", "Please add at least one parasite strain before continuing", QMessageBox.Ok)
            return False
        self.answers, message = databaseConnection.quiz_rows(self.parasiteCriteria, self.noQuestions.value())
        
        if message != "Success":
            QMessageBox.warning(self, "Attention", message, QMessageBox.Ok)
            return False
        
        #Check to see if user wants to test counts
        self.useCount = False
        if self.includeCount.checkState() == 2:
            self.useCount = True

        #Set up quiz viewer and connect this to the quiz parent QDialog
        self.timeAllowed = int(self.minutes.value() * 60) + int(self.seconds.value())
        QMessageBox.warning(self, "Get ready!", "Press OK to start the quiz", QMessageBox.Ok)
        self.newQuiz = myQuestion(self.useCount, self.parasiteCriteria, self.answers, self.error.value(), self.seconds.value(), self.minutes.value())
        self.allowableError = self.error.value()
        self.newQuiz.emitResults.connect(self.on_allResults)
        self.newQuiz.show()

        return True

    # Resets all optional fields to blank/default values
    def resetFields(self):
        self.noQuestions.setValue(10)
        self.error.setValue(0.05)
        self.includeCount.setCheckState(False)
        self.minutes.setValue(5)
        self.seconds.setValue(0)
        self.parasiteCriteria = []
        
    # Closes the application if the esc key is pressed
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.emitClose.emit()  
            self.close()

    # Once the user has submitted their answers in the question class, receives the answers and creates
    # a corresponding results sheet
    @QtCore.pyqtSlot(list)
    def on_allResults(self, returnedValues):
        self.newQuiz.givenAnswers = []
        self.newQuiz.deleteLater()
        self.newQuiz = None

        self.allResults = returnedValues[0]
        timeTaken = self.timeAllowed - returnedValues[1]
        self.resultsSheet = Results(self.allResults, self.answers, self.useCount, self.allowableError, timeTaken)
        self.resultsSheet.emitCloseResults.connect(self.closeResultsWindow)

    # Closes the window and associated objects correctly
    @QtCore.pyqtSlot(list)
    def closeResultsWindow(self):
        self.resultsSheet = None
        self.resetFields
        self.answers = []
        self.allResults = []


    def closeEvent(self, event):
        self.emitClose.emit()  
        event.accept()

