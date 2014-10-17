import sys
#Package containing all list options
from PyQt4 import QtGui, QtCore
from lists import *
#Package for image uploader class
from uploader import *
from browser import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Application(QtGui.QDialog):

  # Constructor
  def __init__(self):
    super(Application, self).__init__()
    self.setStyleSheet('font-size: 11pt; font-family: Arial;')
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
    
    header = QtGui.QLabel('Welcome to the Parasight Image Uploader')
    header.setAlignment(Qt.AlignCenter)
    self.grid.addWidget(header, 1, 1, 1, 6)

    
    self.label = QtGui.QLabel(self)
    self.mainImage = QtGui.QPixmap('Plasmodium_falciparum_01.png')    
    self.mainImageScaled = self.mainImage.scaled(300, 500, Qt.KeepAspectRatio)
    self.label.setPixmap(self.mainImageScaled)
    self.label.setScaledContents(True)
   
    
    self.grid.addWidget(self.label, 2, 1, 1, 6)
    
    uploadButton = self.createButton('Upload Image', self.showImageUploader)
    browseButton = self.createButton('Browse Images', self.showImageBrowser)
    faqButton = self.createButton('FAQ', self.faqInterface)
    contactButton = self.createButton('Contact', self.contactInterface)
  

    self.grid.addWidget(uploadButton, 4, 1, 1, 3)
    self.grid.addWidget(browseButton, 4, 4, 1, 3)
    self.grid.addWidget(faqButton, 5, 1, 1, 3)
    self.grid.addWidget(contactButton, 5, 4, 1, 3)

    footer = QtGui.QLabel('Parasight Project Team 2014')
    footer.setAlignment(Qt.AlignCenter)
    self.grid.addWidget(footer, 6, 1, 1, 6)
   
    self.setLayout(self.grid)
    self.center()
    self.setWindowTitle('Parasight') #Title of the program
    self.setWindowIcon(QtGui.QIcon('logo.jpeg'))
    self.show() #Need this to show window
  
  def showImageUploader(self):
    self.uploader = ImageUploader()
    self.uploader.show()

  def showImageBrowser(self):
    self.browser = ImageBrowser()
    self.browser.show()

  def createButton(self, name, buttonFunction):
    btn = QtGui.QPushButton(name, self)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip('Centers the window on the screen')
    #btn.resize(300, 150)  
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

  def faqInterface(self):
    self.warning('FAQ', 'To be added')

  def contactInterface(self):
    self.warning('Contact', 'To be added')
 
  def warning(self, title, text):
    return QMessageBox.warning(self, title, text, QMessageBox.Ok)
