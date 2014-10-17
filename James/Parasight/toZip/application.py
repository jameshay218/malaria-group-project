# -*- coding: utf-8 -*-
import sys
#Package containing all list options
from PyQt4 import QtGui, QtCore
from lists import *
#Package for image uploader class
from uploader import *
from browser import *
from diagnosis import *
from quiz import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Application(QtGui.QDialog):
  #Manages the other windows
  uploader = None
  browser = None
  quiz = None
  diagnoser = None
  
  # Constructor
  def __init__(self):
    super(Application, self).__init__()
    #Change this to adjust style
    #self.setStyleSheet('font-size: 11pt; font-family: Arial;')
    self.styleData = ''

    f = open('style', 'r')
    self.styleData = f.read()
    f.close()

    self.initUI()

  # Centers the window on the screen
  def center(self):
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  #Sets up the UI
  def initUI(self):
    self.grid = QGridLayout()
    self.grid.setSpacing(10)
    
    #Window image
    self.label = QtGui.QLabel(self)
    self.mainImage = QtGui.QPixmap('images/plas05.jpg')    
    self.scaledMainImage = self.mainImage.scaled(385, 481, Qt.KeepAspectRatio)
    self.label.setPixmap(self.scaledMainImage)
    #self.label.setScaledContents(True)
    self.grid.addWidget(self.label, 2, 1, 1, 6)
    
    #Create buttons to create other windows
    uploadButton = self.createButton('Upload Image', self.showImageUploader, 'Choose an image to upload to the database')
    browseButton = self.createButton('Browse Images', self.showImageBrowser, 'Browse the Parasight image database')
    faqButton = self.createButton('About', self.faqInterface, 'Visit our website')
    contactButton = self.createButton('Contact', self.contactInterface, 'Email us!')
    quizButton = self.createButton('Quiz', self.showQuiz, 'Test your diagnostic accuracy')
    diagnosisButton = self.createButton('Diagnose', self.showDiagnosis, 'Diagnose a local image')

    #Add buttons to layout
    self.grid.addWidget(uploadButton, 4, 1, 1, 3)
    self.grid.addWidget(browseButton, 4, 4, 1, 3)
    self.grid.addWidget(quizButton, 5, 1, 1, 3)
    self.grid.addWidget(diagnosisButton, 5, 4, 1, 3)
    self.grid.addWidget(faqButton, 6, 1, 1, 3)
    self.grid.addWidget(contactButton, 6, 4, 1, 3)

    #Footer information
    footer = QtGui.QLabel('Parasight Project Team 2014')
    footer.setStyleSheet("font-size: 8pt; font-family: Verdana;")
    footer.setAlignment(Qt.AlignCenter)
    self.grid.addWidget(footer, 7, 1, 1, 7)
   
    #PyQt formatting housekeeping
    self.setStyle(QtGui.QStyleFactory.create("plastique"))
    self.setStyleSheet(self.styleData)
    self.setLayout(self.grid)
    self.center()
    self.setWindowTitle('Parasight') #Title of the program
    self.setWindowIcon(QtGui.QIcon('images/logo.png')) #Window icon
    self.show() 
  
  #Displays the Diagnosis tool window
  def showDiagnosis(self):
    if self.diagnoser is not None:
      self.warning("Attention", "The image diagnoser is already running!")
      return
    self.diagnoser = Diagnoser()
    self.diagnoser.emitClose.connect(self.closeDiagnoser)
    self.diagnoser.show()


  #Displays the Image Uploader tool window
  def showImageUploader(self):
    #Only allow one copy of the window to run
    if self.uploader is not None:
      self.warning("Attention", "The image uploader is already running!")
      return
    self.uploader = ImageUploader()
    self.uploader.emitClose.connect(self.closeImageUploader)
    self.uploader.show()


  #Displays the Quiz tool window
  def showQuiz(self):
    if self.quiz is not None:
      self.warning("Attention", "The quiz is already running!")
      return
    self.quiz = Quiz()
    self.quiz.emitClose.connect(self.closeQuiz)
    self.quiz.show()
    
  #Display the image browser window
  def showImageBrowser(self):
    if self.browser is not None:
      self.warning("Attention", "The image uploader is already running!")
      return
    self.browser = ImageBrowser()
    self.browser.emitClose.connect(self.closeImageBrowser)
    self.browser.show()

  #Receives a signal from the uploader object when it is closed
  @QtCore.pyqtSlot(str)
  def closeImageUploader(self):
    self.uploader = None

  @QtCore.pyqtSlot(str)
  def closeImageBrowser(self):
    self.browser = None

  @QtCore.pyqtSlot(str)
  def closeQuiz(self):
    self.quiz = None
 
  @QtCore.pyqtSlot(str)
  def closeDiagnoser(self):
    self.diagnoser = None


  #If escape is pressed, close the application
  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape:
      self.uploader = None
      self.browser = None
      self.quiz = None
      self.diagnoser = None
      self.close()
  
  #Returns a PyQt button with the provided information
  def createButton(self, name, buttonFunction, tooltip):
    btn = QtGui.QPushButton(name, self)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip(tooltip)
    return btn

  #Checks that user wishes to close the application
  def closeEvent(self, event):
    reply = QtGui.QMessageBox.question(self, 'Warning!', \
            "Are you sure that you would like to quit?", \
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
       
    if reply == QtGui.QMessageBox.Yes:
      event.accept()
    else:
      event.ignore() 

  #Displays the FAQ window
  def faqInterface(self):
    QDesktopServices.openUrl(QUrl("http://146.169.44.84:55000"))
    #self.warning('FAQ', 'To be added')

  #Displays the contact information window
  def contactInterface(self):
    QDesktopServices.openUrl(QUrl("mailto:jah113@imperial.ac.uk?subject=&body="))
 
  #Returns a warning message box with the requested text
  def warning(self, title, text):
    return QMessageBox.warning(self, title, text, QMessageBox.Ok)
