import sys
import time
from PIL import Image
import os
import io
from array import array
from database import *
import cPickle as p
from lists import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import base64


MAX_COMMENT_LEN = 100

class ImageUploader(QtGui.QDialog):
  def __init__(self):
    super(ImageUploader, self).__init__()
    # Set the style of the window (font size and type)
    self.setStyleSheet('font-size: 11pt; font-family: Arial;')
    self.uploaderUI()
    self.database = Database()
    
    
  # Function to easily create a button by passing it a name, tooltip
  # and function that is executed on click
  def createButton(self, name, buttonFunction, tooltip):
    btn = QPushButton(name, self)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip(tooltip)
    return btn
  
  # Creates the uploader UI
  def uploaderUI(self):
    labelNames = []
    self.dropdowns = []

    #Creates a list of labels from the FIELD_NAMES list
    for name in FIELD_NAMES:
      labelNames.append(QLabel(name))
      
    #Creates a list of dropdown menus
    for i in range (0, 4):
      self.dropdowns.append(QComboBox(self))
      for option in ALL_FIELDS[i]:
        self.dropdowns[i].addItem(option)
      
    #Creates a grid layout
    self.grid = QGridLayout()
    self.grid.setSpacing(10)
   
    #Add title - do we want to use an image instead?
    titleLabel = QLabel('Malaria Image Uploader')
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
    self.uploadButton = self.createButton('Upload', self.uploadImage, toolTip[j])
    self.resetButton = self.createButton('Reset', self.resetFields, toolTip[j+1])
      
    self.closeButton = self.createButton('Close', self.close, toolTip[j+2])
    self.grid.addWidget(self.uploadButton, j+3, 1)
    self.grid.addWidget(self.resetButton, j+3, 2)
    self.grid.addWidget(self.closeButton, j+3, 3)

    #Display housekeeping
    self.setLayout(self.grid)
    self.move(300, 150)
    self.setWindowTitle('Parasight Image Uploader') #Title of the program
    self.setWindowIcon(QIcon('icon.png'))
    #self.show() 

  
  def findFile(self):
    self.fileDialog = QFileDialog(self)
    filename = self.fileDialog.getOpenFileName()
    self.fileLine.setText(filename)
    
  
  def uploadImage(self):
    labels = []
    #Make sure that a valid file type has been selected
    if not QFile.exists(self.fileLine.text()):
      #self.warning('Attention', 'Invalid file selected')
      return False
    if not(self.fileCheck(self.fileLine.text())):
      #self.warning('Attention', 'Invalid file type')
      return False
    #Need to do a size check?
    for field in self.dropdowns:     
      if field.currentText() == '<Please select one>':
        #self.warning('Attention', 'Please ensure that all fields are complete. If no labels are applicable, choose NULL.')
        return False
    

    #Convert the image into a byte array for storage in the db
    bytes = self.readimage(self.fileLine.text())
 
    #print(self.fileLine.text())
    labels.append(time.strftime("%d-%m-%Y"))
    for field in self.dropdowns:     
      labels.append(str(field.currentText()))
    labels.append(str(self.countSlide.value()))
    labels.append(str(self.totalZoom.value()))
    labels.append(str(self.slideID.text()))
    
    comment = self.otherComments.toPlainText()
    if len(comment) > MAX_COMMENT_LEN:
      #self.warning('Attention', 'Please limit comment length to ' + `MAX_COMMENT_LEN` + ' words')
      return False
    labels.append(str(self.otherComments.toPlainText()))

    #print 'Labels: ' + `labels`
    success = self.database.insert_create(labels, bytes)
    if success != "Success":
      #self.warning('Attention', success)
      return False
    return True

  
  def resetFields(self):
    self.fileLine.setText('')
    for field in self.dropdowns:
        field.setCurrentIndex(0)
    self.countSlide.setValue(0)
    self.totalZoom.setValue(0)
    self.slideID.clear()
    self.otherComments.clear()
       

        
  def warning(self, title, text):
    return QMessageBox.warning(self, title, text, QMessageBox.Ok)


  def fileCheck(self, path):
   for filetype in FILE_TYPES:
     if path.endsWith(filetype):
       return True
   return False      
        
  def readimage(self, path):
    with open(path, "rb") as f:
      #print 'Made byte array from ' + `path`
      return base64.b64encode(f.read())

