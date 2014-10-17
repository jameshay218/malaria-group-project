import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import database
import browser
import uploader
from application import *
import base64
from lists import *

class TestApplication(unittest.TestCase):
    
    '''def __init__(self):
        self.test_application = None
        qApp = None
    '''
    def setUp(self):
        self.test_application = QApplication(sys.argv)
        self.test_application = Application()
        
    def test_application_1(self):
        self.test_application.closeEvent(close())

    def tearDown(self):
        self.test_application.close
                   
    
if __name__ == '__main__':
    unittest.main()
   
