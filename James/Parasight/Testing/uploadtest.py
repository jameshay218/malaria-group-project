import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import database
import browser
import uploader
import application
import base64
from lists import *

# Upload successes
uploadSuccess1 = (['12-03-2014', 1, 1, 1, 1, 0.5, 63, 'uploadSuccess1', 'thisisatest'], True, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/logo.jpeg')
uploadSuccess2 = (['12-03-2014', 1, 2, 2, 1, 0.0, 80, 'uploadSuccess2', 'thisisatest2'], True, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/Plasmodium_falciparum_01.png')
uploadSuccess3 = (['12-03-2014', 1, 1, 1, 1, 0.8, 10, 'uploadSuccess3', 'thisisatest3'], True, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadSuccess4 = (['12-03-2014', 1, 2, 1, 2, 0.0, 10, '', ''], True, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadSuccess5 = (['12-03-2014', 1, 1, 1, 1, 0.8, 10, 'uploadSuccess5', 'thisisatest5'], True, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadSuccesses = [uploadSuccess1, uploadSuccess2, uploadSuccess3, uploadSuccess4, uploadSuccess5]

#Upload failures
uploadFailure1 =  (['', 0, 0, 0, 0, 0.0, 1, '', ''], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/logo.jpeg')
uploadFailure2 = (['12-03-2014', 1, 1, 1, 1, 0.8, 10, 'uploadFailure2;', 'thisisatest7'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure3 = (['12-03-2014', 1, 1, 1, 1, 0.8, 10, 'uploadFailure3', 'thisisatest8;'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure4 = (['12-03-2014', 1, 1, 1, 0, 0.8, 10, 'uploadFailure4', 'thisisatest8;'],False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure5 = (['12-03-2014', 1, 1, 1, 1, 2.0, 10, 'uploadFailure5', 'thisisatest9;'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure6 = (['12-03-2014', 1, 1, 1, 1, 1.0, 0, 'uploadFailure6', 'thisisatest10;'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure7 = (['12-03-2014', 1, 1, 1, 1, 1.0, 10000001, 'uploadFailure7', 'thisisatest11;'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')
uploadFailure8 = (['12-03-2014', 1, 1, 1, 1, 1.0, 10, 'uploadFailure8', 'thisisatest12;'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/shouldnotwork.txt')
uploadFailure9 = (['12-03-2014', 2, 1, 1, 1, 0.8, 10, 'uploadFailure9', 'thisisatest13'], False, '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/Upload Test Images/testsave.jpg')

uploadFailures = [uploadFailure1, uploadFailure2,uploadFailure3, uploadFailure4, uploadFailure5, uploadFailure6, uploadFailure7, uploadFailure8, uploadFailure9] 

class TestUploader(unittest.TestCase):
    
    '''def __init__(self):
        self.test_application = None
        qApp = None
    '''
    def setUp(self):
        self.test_application = QApplication(sys.argv)
        #qApp = self.test_application
        self.test_application.uploader = uploader.ImageUploader()
        self.test_uploader = self.test_application.uploader
        #return self.test_application
        

    
    def test_upload_success1_jpeg(self):
        self.test_uploader.fileLine.setText(uploadSuccesses[0][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadSuccesses[0][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadSuccesses[0][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadSuccesses[0][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadSuccesses[0][0][4])
        self.test_uploader.countSlide.setValue(uploadSuccesses[0][0][5])
        self.test_uploader.totalZoom.setValue(uploadSuccesses[0][0][6])
        self.test_uploader.slideID.setText(uploadSuccesses[0][0][7])
        self.test_uploader.otherComments.setText(uploadSuccesses[0][0][8])
        self.assertTrue(self.test_uploader.uploadImage())

        
    def test_upload_success2_png(self):
        self.test_uploader.fileLine.setText(uploadSuccesses[1][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadSuccesses[1][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadSuccesses[1][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadSuccesses[1][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadSuccesses[1][0][4])
        self.test_uploader.countSlide.setValue(uploadSuccesses[1][0][5])
        self.test_uploader.totalZoom.setValue(uploadSuccesses[1][0][6])
        self.test_uploader.slideID.setText(uploadSuccesses[1][0][7])
        self.test_uploader.otherComments.setText(uploadSuccesses[1][0][8])
        self.assertTrue(self.test_uploader.uploadImage())

    
    def test_upload_success3_jpg(self):
        self.test_uploader.fileLine.setText(uploadSuccesses[2][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadSuccesses[2][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadSuccesses[2][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadSuccesses[2][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadSuccesses[2][0][4])
        self.test_uploader.countSlide.setValue(uploadSuccesses[2][0][5])
        self.test_uploader.totalZoom.setValue(uploadSuccesses[2][0][6])
        self.test_uploader.slideID.setText(uploadSuccesses[2][0][7])
        self.test_uploader.otherComments.setText(uploadSuccesses[2][0][8])
        self.assertTrue(self.test_uploader.uploadImage())


    def test_upload_success4_blankoptionalfields(self):
        self.test_uploader.fileLine.setText(uploadSuccesses[3][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadSuccesses[3][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadSuccesses[3][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadSuccesses[3][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadSuccesses[3][0][4])
        self.test_uploader.countSlide.setValue(uploadSuccesses[3][0][5])
        self.test_uploader.totalZoom.setValue(uploadSuccesses[3][0][6])
        self.test_uploader.slideID.setText(uploadSuccesses[3][0][7])
        self.test_uploader.otherComments.setText(uploadSuccesses[3][0][8])
        self.assertTrue(self.test_uploader.uploadImage())


    def test_upload_success5_identicalimage(self):
        self.test_uploader.fileLine.setText(uploadSuccesses[4][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadSuccesses[4][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadSuccesses[4][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadSuccesses[4][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadSuccesses[4][0][4])
        self.test_uploader.countSlide.setValue(uploadSuccesses[4][0][5])
        self.test_uploader.totalZoom.setValue(uploadSuccesses[4][0][6])
        self.test_uploader.slideID.setText(uploadSuccesses[4][0][7])
        self.test_uploader.otherComments.setText(uploadSuccesses[4][0][8])
        self.assertTrue(self.test_uploader.uploadImage())
        
    
    def test_reset(self):
        self.assertEqual(self.test_uploader.fileLine.text(), '')
        self.assertEqual(self.test_uploader.dropdowns[0].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[1].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[2].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[3].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.countSlide.value(), 0.0)
        self.assertEqual(self.test_uploader.totalZoom.value(), 1)
        self.assertEqual(str(self.test_uploader.slideID.text()), '')
        self.assertEqual(str(self.test_uploader.otherComments.toPlainText()), '')
        self.assertFalse(self.test_uploader.uploadImage())
        test = uploadSuccesses[0]
        self.test_uploader.fileLine.setText(test[2])
        self.test_uploader.dropdowns[0].setCurrentIndex(test[0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(test[0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(test[0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(test[0][4])
        self.test_uploader.countSlide.setValue(test[0][5])
        self.test_uploader.totalZoom.setValue(test[0][6])
        self.test_uploader.slideID.setText(test[0][7])
        self.test_uploader.otherComments.setText(test[0][8])
        self.assertTrue(self.test_uploader.uploadImage())
        QTest.mouseClick(self.test_uploader.resetButton, Qt.LeftButton)
        self.assertEqual(self.test_uploader.fileLine.text(), '')
        self.assertEqual(self.test_uploader.dropdowns[0].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[1].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[2].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.dropdowns[3].currentText(), '<Please select one>')
        self.assertEqual(self.test_uploader.countSlide.value(), 0.0)
        self.assertEqual(self.test_uploader.totalZoom.value(), 1)
        self.assertEqual(str(self.test_uploader.slideID.text()), '')
        self.assertEqual(str(self.test_uploader.otherComments.toPlainText()), '')
     
    def test_upload_failure1_blankfields(self):
        self.test_uploader.fileLine.setText(uploadFailures[0][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[0][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[0][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[0][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[0][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[0][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[0][0][6])
        self.test_uploader.slideID.setText(uploadFailures[0][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[0][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

     
    def test_upload_failure2_semicolon1(self):
        self.test_uploader.fileLine.setText(uploadFailures[1][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[1][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[1][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[1][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[1][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[1][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[1][0][6])
        self.test_uploader.slideID.setText(uploadFailures[1][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[1][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

    def test_upload_failure3_semicolon2(self):
        self.test_uploader.fileLine.setText(uploadFailures[2][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[2][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[2][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[2][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[2][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[2][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[2][0][6])
        self.test_uploader.slideID.setText(uploadFailures[2][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[2][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

    def test_upload_failure4_blankfield(self):
        self.test_uploader.fileLine.setText(uploadFailures[3][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[3][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[3][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[3][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[3][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[3][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[3][0][6])
        self.test_uploader.slideID.setText(uploadFailures[3][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[3][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

     
    def test_upload_failure5_outofrange1(self):
        self.test_uploader.fileLine.setText(uploadFailures[4][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[4][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[4][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[4][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[4][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[4][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[4][0][6])
        self.test_uploader.slideID.setText(uploadFailures[4][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[4][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

    def test_upload_failure6_outofrange2(self):
        self.test_uploader.fileLine.setText(uploadFailures[5][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[5][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[5][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[5][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[5][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[5][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[5][0][6])
        self.test_uploader.slideID.setText(uploadFailures[5][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[5][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

    def test_upload_failure7_outofrange3(self):
        self.test_uploader.fileLine.setText(uploadFailures[6][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[6][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[6][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[6][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[6][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[6][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[6][0][6])
        self.test_uploader.slideID.setText(uploadFailures[6][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[6][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

     
    def test_upload_failure8_invalidfile(self):
        self.test_uploader.fileLine.setText(uploadFailures[7][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[7][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[7][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[7][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[7][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[7][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[7][0][6])
        self.test_uploader.slideID.setText(uploadFailures[7][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[7][0][8])
        self.assertFalse(self.test_uploader.uploadImage())

    def test_upload_failure9_fieldtoolong(self):
        self.test_uploader.fileLine.setText(uploadFailures[8][2])
        self.test_uploader.dropdowns[0].setCurrentIndex(uploadFailures[8][0][1])
        self.test_uploader.dropdowns[1].setCurrentIndex(uploadFailures[8][0][2])
        self.test_uploader.dropdowns[2].setCurrentIndex(uploadFailures[8][0][3])
        self.test_uploader.dropdowns[3].setCurrentIndex(uploadFailures[8][0][4])
        self.test_uploader.countSlide.setValue(uploadFailures[8][0][5])
        self.test_uploader.totalZoom.setValue(uploadFailures[8][0][6])
        self.test_uploader.slideID.setText(uploadFailures[8][0][7])
        self.test_uploader.otherComments.setText(uploadFailures[8][0][8])
        self.assertFalse(self.test_uploader.uploadImage())


    def test_close(self):
        QTest.mouseClick(self.test_uploader.closeButton, Qt.LeftButton)
    
    def tearDown(self):
        self.test_application.uploader.close
        self.test_uploader.close
                
    
if __name__ == '__main__':
    unittest.main()
   

    
