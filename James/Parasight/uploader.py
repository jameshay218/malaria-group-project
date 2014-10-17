import sys
import time
from PIL import Image
import os
import io
from array import array
from database import *
from question import *
import cPickle as p
from lists import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import base64
from imagemanager import *

MAX_COMMENT_LEN = 100

class ImageUploader(ImageManager):
  emitClose = QtCore.pyqtSignal()
  emitProgressUpdate = QtCore.pyqtSignal(int)
  loadingBar = None

  def __init__(self):
    super(ImageUploader, self).__init__()
    # Set the style of the window (font size and type)
    #self.setStyleSheet('font-size: 11pt; font-family: Arial;')
    self.styleData = ''
         
    f = open('style', 'r')
    self.styleData = f.read()
    f.close()
        
    self.initUI()
    self.database = Database()
       
 
  # Creates the uploader UI
  def initUI(self):
    labelNames = []
    self.dropdowns = []

    #Creates a list of labels from the FIELD_NAMES list
    for name in FIELD_NAMES:
      labelNames.append(QLabel(name))

    for label in labelNames:
      label.setAlignment(Qt.AlignTop)
      
    #Creates a list of dropdown menus
    for i in range (0, 4):
      self.dropdowns.append(QComboBox(self))
      for option in ALL_FIELDS[i]:
        self.dropdowns[i].addItem(option)
      
    #Creates a grid layout
    self.grid = QGridLayout()
    self.grid.setSpacing(10)
   
    #Add title - do we want to use an image instead?
    titleLabel = QLabel(self)
    self.bannerImage = QtGui.QPixmap('images/imageUploaderTrans.png')
    self.bannerImageScaled = self.bannerImage.scaled(250, 60, Qt.KeepAspectRatio)
    titleLabel.setPixmap(self.bannerImageScaled)
    #titleLabel.setAlignment(QtCore.Qt.AlignCenter)
    self.grid.addWidget(titleLabel, 0, 0, 1, 4, QtCore.Qt.AlignCenter)
    
    #Add widget to allow image to be uploaded from directory
    self.grid.addWidget(QLabel('Image Location'), 2, 0)
    self.fileLine = QLineEdit(self)
    self.grid.addWidget(self.fileLine, 2, 1, 1, 2)
    self.grid.addWidget(self.createButton('Locate', self.findFile, toolTip[0]), 2, 3)

    #Create dropdown menus
    j = 0
    l = 3
    for name in labelNames:
      #Add label to line
      self.grid.addWidget(labelNames[j], l, 0)
      #For first 4 labels, add dropdown menus
      if j < 4:
        self.grid.addWidget(self.dropdowns[j], l, 1, 1, 3)
      #Then add the count input
      elif j == 4:
        self.countSlide = QDoubleSpinBox()
        self.countSlide.setRange(0, 1)
        self.countSlide.setDecimals(3)
        self.countSlide.setSingleStep(0.001)
        self.grid.addWidget(self.countSlide, l, 1, 1, 1)
      #Zoom input
      elif j == 5:
        self.totalZoom = QSpinBox()
        self.totalZoom.setRange(1, 1000000)
        self.grid.addWidget(self.totalZoom, l, 1, 1, 1)
      #Allow custom slide ID
      elif j == 6:
        self.slideID = QLineEdit()
        self.slideID.setMaxLength(25)
        self.grid.addWidget(self.slideID, l, 1, 1, 3)
      #Allow user to add additional comments
      elif j == 7:
        self.otherComments = QTextEdit()
        self.grid.addWidget(self.otherComments, l, 1, 1, 3)

      j = j + 1
      l = l + 1

    #Add the management buttons at the bottom
    self.uploadButton = self.createButton('Upload', self.uploadImage, 'Submits an upload request to the database')
    self.resetButton = self.createButton('Reset', self.resetFields, 'Resets all fields')
                           
    self.grid.addWidget(self.uploadButton, j+3, 1)
    self.grid.addWidget(self.resetButton, j+3, 2)
    self.grid.addWidget(self.createButton('Close', self.closeWindow, 'Closes the window'), j+3, 3)
    
    #Display housekeeping
    self.setStyle(QtGui.QStyleFactory.create("Plastique"))
    self.setStyleSheet(self.styleData)
    self.setLayout(self.grid)
    self.move(300, 150)
    self.setWindowTitle('Parasight Image Uploader') #Title of the program
    self.setWindowIcon(QIcon('images/logo.png'))
    self.show() 

  
    
        
  # Submits an upload query to the database interface class and returns true if the query is
  # successfully submitted. Carries out a number of validity checks
  def uploadImage(self):
    labels = []
    # If no file has been specified, abort upload
    if self.fileLine.text() == '':
      self.warning('Attention', 'Please select a file')
      return False
    
    # Display loading/progress bar for slower uploads or multiple files
    self.loadingBar = ProgressBar(len(self.filenameString))
    self.emitProgressUpdate.connect(self.loadingBar.updateProgress)
    fileno = 1

    # For each specified file, make sure that a valid file type has been selected      
    for filename in self.filenameString:
      # If file does not exist, return false
      if not QFile.exists(filename):
        self.loadingBar = None
        self.warning('Attention', 'Invalid file selected: ' + `filename`)
        return False
      # Pass file name to file check function
      if not self.fileCheck(filename):
        self.loadingBar = None
        self.warning('Attention', 'Invalid file type: ' + `filename`)
        return False
    
      # Warn if a file label has not been filled in
      for field in self.dropdowns:     
        if field.currentText() == '<Please select one>':
          self.loadingBar = None
          self.warning('Attention', 'Please ensure that all fields are complete. If no labels are applicable, choose NULL.')
          return False
        
        
    #Convert the image into a byte array for storage in the db
      bytes = self.readimage(filename)
            
      # Go through all of the user provided labels and add these to a list to be passed to the
      # database class
      labels.append(time.strftime("%d-%m-%Y"))
      for field in self.dropdowns:     
        labels.append(str(field.currentText()))
      labels.append(str(self.countSlide.value()))
      labels.append(str(self.totalZoom.value()))
      labels.append(str(self.slideID.text()))
    
      comment = self.otherComments.toPlainText()
      # Make sure that provided comment is not too long
      if len(comment) > MAX_COMMENT_LEN:
        self.warning('Attention', 'Please limit comment length to ' + `MAX_COMMENT_LEN` + ' words')
        self.loadingBar = None
        return False
      labels.append(str(self.otherComments.toPlainText()))

      # Pass list to database class to form an SQL query. If "Success" is not the returned message,
      # display the error message as a warning box and 
      success = self.database.insert_create(labels, bytes)
      if success != "Success":
        self.loadingBar = None
        self.warning('Attention', 'Uploading file ' + `filename` + ': ' + `success`)
        return False
      labels = []
      self.emitProgressUpdate.emit(fileno)
      
      fileno += 1
      
    # If all has worked out, remove the loading bar and display a success message
    self.loadingBar.deleteLater()
    self.loadingBar = None
    self.warning('Great!', success)
    return True

  # Opens a file dialog to allow user to locate a file from the file system. Sets the text of the 
  # filename line to the file address, or displays the number of selected files if greater
  # than one
  def findFile(self):
    self.fileDialog = QFileDialog(self)
    filenames = self.fileDialog.getOpenFileNames()
    self.filenameString = map(str, filenames)
    #print self.filenameString
    if len(self.filenameString) == 1:
      self.fileLine.setText(self.filenameString[0])
    else:
      self.fileLine.setText('Files selected: ' + `len(self.filenameString)`)



  # Resets all of the optional fields
  def resetFields(self):
    self.fileLine.setText('')
    for field in self.dropdowns:
        field.setCurrentIndex(0)
    self.countSlide.setValue(0)
    self.totalZoom.setValue(0)
    self.slideID.clear()
    self.otherComments.clear()
       
  # Checks the provided file path against the allowable file types in lists.py
  def fileCheck(self, path):
   for filetype in FILE_TYPES:
     if path.endswith(filetype):
       return True
   return False      
        
  # Creates a byte array from the provided file path
  def readimage(self, path):
    with open(path, "rb") as f:
      return base64.b64encode(f.read())


# Small helper class for uploader.py to track uploading of images
class ProgressBar(QtGui.QWidget):
  
  def __init__(self, maxFiles):
    super(ProgressBar, self).__init__()
    self.styleData = ''
         
    f = open('style', 'r')
    self.styleData = f.read()
    f.close()
        
    self.initUI(maxFiles)

  def initUI(self, maxFiles):
    self.pbar = QtGui.QProgressBar(self)
    self.pbar.setGeometry(30, 40, 200, 25)
    self.pbar.setMinimum(0)
    self.pbar.setMaximum(maxFiles)
    self.pbar.setValue(0)
    self.setStyleSheet(self.styleData)
    self.setWindowTitle('Loading') #Title of the program
    self.setWindowIcon(QtGui.QIcon('images/logo.png'))
    self.show()

  # Slot connected to the uploader class to continually update progress
  @QtCore.pyqtSlot(int)
  def updateProgress(self, progress):
    self.pbar.setValue(progress)
    if progress == self.pbar.maximum():
      self.close()

   
