#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
James Hay Python GUI Practice

author: James Hay
last edited: 29/01/2014
"""

import sys
#Package containing all list options
from lists import *
#Package for image uploader class
from uploader import *
from browser import *
from application import *
from PyQt4 import QtGui, QtCore

"""
Class containing methods for the main application
"""

# Creates an application window
def main():
  app = QtGui.QApplication(sys.argv)
  ex = Application()
  #uploader = ImageUploader()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
