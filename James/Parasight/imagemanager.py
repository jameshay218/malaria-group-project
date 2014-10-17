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
import thread
import csv

# Parent class of the uploader, browser and diagnose class
class ImageManager(QtGui.QDialog):
    # Function to easily create a button by passing it a name, tooltip
    # and function that is executed on click
    def createButton(self, name, buttonFunction, tooltip):
        btn = QPushButton(name, self)
        btn.clicked.connect(buttonFunction)
        btn.setToolTip(tooltip)
        return btn

    # Informations the owner application that window is closing
    def closeWindow(self):
        self.emitClose.emit()
        self.close()
 
    # Informs the owner application that window is closing when a close event is initiated
    def closeEvent(self, event):
        self.emitClose.emit()  
        event.accept()

    # Closes the window when the escape key is pressed
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.emitClose.emit()  
            self.close()
    
    # Creates a warning box with given text and title
    def warning(self, title, text):
        return QMessageBox.warning(self, title, text, QMessageBox.Ok)
