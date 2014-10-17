from lists import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
   
class WaitingBar(QtGui.QDialog):
  
  def __init__(self, maxFiles):
    super(WaitingBar, self).__init__()
    self.styleData = ''

    f = open('style', 'r')
    self.styleData = f.read()
    f.close()
    self.initUI(maxFiles)
    
        
  def initUI(self, maxFiles):
    self.pbar = QtGui.QProgressBar(self)
    self.pbar.resize(225, 25)
    self.setGeometry(0, 0, 225, 25)
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
    self.pbar.setMinimum(0)
    self.pbar.setMaximum(maxFiles)
    self.setStyleSheet(self.styleData)
    self.setWindowTitle('Loading. Please wait!')
    self.setWindowIcon(QtGui.QIcon('images/logo.png'))
    self.show()
    
