import sys
import os
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt, QDate, QFile
import database
import browser
import uploader
import application
import base64
from lists import *

# Search successes
searchSuccess1 = ['01-01-2013;13-03-2014', 'NULL', 'NULL', 'NULL', 'NULL', '0.0;1.0', '0;1000000', 'NULL', 'NULL']
searchSuccess2 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Test!', 'NULL']
searchSuccess3 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Doesnotexist', 'NULL']
searchSuccess4 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 0.0, 1, 1000000, 'NULL', 'NULL']
searchSuccess5 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 63, 63, 'NULL', 'NULL']
searchSuccess6 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 1, 0, 0, 0.0, 1.0, 1, 1000000, 'NULL', 'NULL']
searchSuccess7 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 1, 0, 0.0, 1.0, 1, 1000000, 'NULL', 'NULL']
searchSuccess8 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 1, 0.0, 1.0, 1, 1000000, 'NULL', 'NULL']
searchSuccess9 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 1, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'NULL', 'NULL']


#Search failures
searchFailure1 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'test;', 'NULL']
searchFailure2 = [QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'NULL', 'test;']


# Download successes
downloadSuccess = ([QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Test!', 'NULL'], '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing/')

# Download failure
downloadFailure1 = ([QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Test!', 'NULL'], '<Download Location>')
downloadFailure2 = ([QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Test!', 'NULL'], 'Should Fail')
downloadFailure3 = ([QDate(2013, 1, 1), QDate(2014, 3, 13), 0, 0, 0, 0, 0.0, 1.0, 1, 1000000, 'Test!', 'NULL'], '/homes/jah113/Malaria/group-project/James/Plaspodium/Testing')


class TestBrowser(unittest.TestCase):
    
    def setUp(self):
        self.test_application = QApplication(sys.argv)
        self.test_application.browser = browser.ImageBrowser()
        self.test_browser = self.test_application.browser
    
    def test_reset_button(self):
        self.test_browser.lowerDate.setDate(QDate(2013, 3, 3))
        self.test_browser.upperDate.setDate(QDate(2013, 5, 5))
        self.test_browser.upperCount.setValue(0.5)
        self.test_browser.lowerCount.setValue(0.5)
        self.test_browser.lowerZoom.setValue(60)
        self.test_browser.upperZoom.setValue(60)
        self.test_browser.slideID.setText('Test!')
        self.test_browser.otherComments.setText('')
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(1)
        self.test_browser.dropdowns[1].setCurrentIndex(1)
        self.test_browser.dropdowns[2].setCurrentIndex(1)
        self.test_browser.dropdowns[3].setCurrentIndex(1)
        self.assertTrue(self.test_browser.imageSearch())
        self.test_browser.resetFields()

        self.assertEqual(QDate.toString(self.test_browser.lowerDate.date(), "dd-MM-yyyy"), "01-01-2013")
        self.assertEqual(QDate.toString(self.test_browser.upperDate.date(), "dd-MM-yyyy"), "13-03-2014")
        self.assertEqual(self.test_browser.dropdowns[0].currentText(), '<Please select one>')
        self.assertEqual(self.test_browser.dropdowns[1].currentText(), '<Please select one>')
        self.assertEqual(self.test_browser.dropdowns[2].currentText(), '<Please select one>')
        self.assertEqual(self.test_browser.dropdowns[3].currentText(), '<Please select one>')
        self.assertEqual(self.test_browser.upperCount.value(), 1.0)
        self.assertEqual(self.test_browser.lowerCount.value(), 0.0)
        self.assertEqual(self.test_browser.lowerZoom.value(), 0)
        self.assertEqual(self.test_browser.upperZoom.value(), 1000000)
        self.assertEqual(self.test_browser.slideID.text(), '')
        self.assertEqual(self.test_browser.otherComments.toPlainText(), '')
        self.assertEqual(self.test_browser.saveLocation.text(), '<Download Location>')
        
    def test_search_success1_allimages(self):
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success2_knownimage(self):
        self.test_browser.lowerDate.setDate(searchSuccess2[0])
        self.test_browser.upperDate.setDate(searchSuccess2[1])
        self.test_browser.upperCount.setValue(searchSuccess2[7])
        self.test_browser.lowerCount.setValue(searchSuccess2[6])
        self.test_browser.lowerZoom.setValue(searchSuccess2[8])
        self.test_browser.upperZoom.setValue(searchSuccess2[9])
        self.test_browser.slideID.setText(searchSuccess2[10])
        self.test_browser.otherComments.setText(searchSuccess2[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess2[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess2[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess2[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess2[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success3_doesnotexist(self):
        self.test_browser.lowerDate.setDate(searchSuccess3[0])
        self.test_browser.upperDate.setDate(searchSuccess3[1])
        self.test_browser.upperCount.setValue(searchSuccess3[7])
        self.test_browser.lowerCount.setValue(searchSuccess3[6])
        self.test_browser.lowerZoom.setValue(searchSuccess3[8])
        self.test_browser.upperZoom.setValue(searchSuccess3[9])
        self.test_browser.slideID.setText(searchSuccess3[10])
        self.test_browser.otherComments.setText(searchSuccess3[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess3[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess3[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess3[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess3[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success4_samecountbound(self):
        self.test_browser.lowerDate.setDate(searchSuccess4[0])
        self.test_browser.upperDate.setDate(searchSuccess4[1])
        self.test_browser.upperCount.setValue(searchSuccess4[7])
        self.test_browser.lowerCount.setValue(searchSuccess4[6])
        self.test_browser.lowerZoom.setValue(searchSuccess4[8])
        self.test_browser.upperZoom.setValue(searchSuccess4[9])
        self.test_browser.slideID.setText(searchSuccess4[10])
        self.test_browser.otherComments.setText(searchSuccess4[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess4[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess4[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess4[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess4[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success5_samezoombound(self):
        self.test_browser.lowerDate.setDate(searchSuccess5[0])
        self.test_browser.upperDate.setDate(searchSuccess5[1])
        self.test_browser.upperCount.setValue(searchSuccess5[7])
        self.test_browser.lowerCount.setValue(searchSuccess5[6])
        self.test_browser.lowerZoom.setValue(searchSuccess5[8])
        self.test_browser.upperZoom.setValue(searchSuccess5[9])
        self.test_browser.slideID.setText(searchSuccess5[10])
        self.test_browser.otherComments.setText(searchSuccess5[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess5[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess5[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess5[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess5[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success6_firstdropdownonly(self):
        self.test_browser.lowerDate.setDate(searchSuccess6[0])
        self.test_browser.upperDate.setDate(searchSuccess6[1])
        self.test_browser.upperCount.setValue(searchSuccess6[7])
        self.test_browser.lowerCount.setValue(searchSuccess6[6])
        self.test_browser.lowerZoom.setValue(searchSuccess6[8])
        self.test_browser.upperZoom.setValue(searchSuccess6[9])
        self.test_browser.slideID.setText(searchSuccess6[10])
        self.test_browser.otherComments.setText(searchSuccess6[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess6[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess6[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess6[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess6[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success7_seconddowndownonly(self):
        self.test_browser.lowerDate.setDate(searchSuccess7[0])
        self.test_browser.upperDate.setDate(searchSuccess7[1])
        self.test_browser.upperCount.setValue(searchSuccess7[7])
        self.test_browser.lowerCount.setValue(searchSuccess7[6])
        self.test_browser.lowerZoom.setValue(searchSuccess7[8])
        self.test_browser.upperZoom.setValue(searchSuccess7[9])
        self.test_browser.slideID.setText(searchSuccess7[10])
        self.test_browser.otherComments.setText(searchSuccess7[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess7[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess7[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess7[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess7[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success8_thirddownonly(self):
        self.test_browser.lowerDate.setDate(searchSuccess8[0])
        self.test_browser.upperDate.setDate(searchSuccess8[1])
        self.test_browser.upperCount.setValue(searchSuccess8[7])
        self.test_browser.lowerCount.setValue(searchSuccess8[6])
        self.test_browser.lowerZoom.setValue(searchSuccess8[8])
        self.test_browser.upperZoom.setValue(searchSuccess8[9])
        self.test_browser.slideID.setText(searchSuccess8[10])
        self.test_browser.otherComments.setText(searchSuccess8[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess8[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess8[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess8[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess8[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_success9_fourthdropdownonly(self):
        self.test_browser.lowerDate.setDate(searchSuccess9[0])
        self.test_browser.upperDate.setDate(searchSuccess9[1])
        self.test_browser.upperCount.setValue(searchSuccess9[7])
        self.test_browser.lowerCount.setValue(searchSuccess9[6])
        self.test_browser.lowerZoom.setValue(searchSuccess9[8])
        self.test_browser.upperZoom.setValue(searchSuccess9[9])
        self.test_browser.slideID.setText(searchSuccess9[10])
        self.test_browser.otherComments.setText(searchSuccess9[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchSuccess9[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchSuccess9[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchSuccess9[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchSuccess9[5])
        self.assertTrue(self.test_browser.imageSearch())

    def test_search_failure1_invalidparameters1(self):
        self.test_browser.lowerDate.setDate(searchFailure1[0])
        self.test_browser.upperDate.setDate(searchFailure1[1])
        self.test_browser.upperCount.setValue(searchFailure1[7])
        self.test_browser.lowerCount.setValue(searchFailure1[6])
        self.test_browser.lowerZoom.setValue(searchFailure1[8])
        self.test_browser.upperZoom.setValue(searchFailure1[9])
        self.test_browser.slideID.setText(searchFailure1[10])
        self.test_browser.otherComments.setText(searchFailure1[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchFailure1[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchFailure1[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchFailure1[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchFailure1[5])
        self.assertFalse(self.test_browser.imageSearch())

    def test_search_failure2_invalidparameters2(self):
        self.test_browser.lowerDate.setDate(searchFailure2[0])
        self.test_browser.upperDate.setDate(searchFailure2[1])
        self.test_browser.upperCount.setValue(searchFailure2[7])
        self.test_browser.lowerCount.setValue(searchFailure2[6])
        self.test_browser.lowerZoom.setValue(searchFailure2[8])
        self.test_browser.upperZoom.setValue(searchFailure2[9])
        self.test_browser.slideID.setText(searchFailure2[10])
        self.test_browser.otherComments.setText(searchFailure2[11])
        self.test_browser.saveLocation.setText('Something')
        self.test_browser.dropdowns[0].setCurrentIndex(searchFailure2[2])
        self.test_browser.dropdowns[1].setCurrentIndex(searchFailure2[3])
        self.test_browser.dropdowns[2].setCurrentIndex(searchFailure2[4])
        self.test_browser.dropdowns[3].setCurrentIndex(searchFailure2[5])
        self.assertFalse(self.test_browser.imageSearch())
    
    
    def test_download_success(self):
        filePath = downloadSuccess[1] + '149'
        if os.path.isfile(filePath):
            try:
                os.remove(filePath)
            except OSError:
                pass
        self.test_browser.lowerDate.setDate(downloadSuccess[0][0])
        self.test_browser.upperDate.setDate(downloadSuccess[0][1])
        self.test_browser.upperCount.setValue(downloadSuccess[0][7])
        self.test_browser.lowerCount.setValue(downloadSuccess[0][6])
        self.test_browser.lowerZoom.setValue(downloadSuccess[0][8])
        self.test_browser.upperZoom.setValue(downloadSuccess[0][9])
        self.test_browser.slideID.setText(downloadSuccess[0][10])
        self.test_browser.otherComments.setText(downloadSuccess[0][11])
        self.test_browser.saveLocation.setText(downloadSuccess[1])
        self.test_browser.dropdowns[0].setCurrentIndex(downloadSuccess[0][2])
        self.test_browser.dropdowns[1].setCurrentIndex(downloadSuccess[0][3])
        self.test_browser.dropdowns[2].setCurrentIndex(downloadSuccess[0][4])
        self.test_browser.dropdowns[3].setCurrentIndex(downloadSuccess[0][5])
        self.assertTrue(self.test_browser.imageSearch())
        self.assertTrue(self.test_browser.imageDownload())
       
    def test_download_failure1(self):
        self.test_browser.lowerDate.setDate(downloadFailure1[0][0])
        self.test_browser.upperDate.setDate(downloadFailure1[0][1])
        self.test_browser.upperCount.setValue(downloadFailure1[0][7])
        self.test_browser.lowerCount.setValue(downloadFailure1[0][6])
        self.test_browser.lowerZoom.setValue(downloadFailure1[0][8])
        self.test_browser.upperZoom.setValue(downloadFailure1[0][9])
        self.test_browser.slideID.setText(downloadFailure1[0][10])
        self.test_browser.otherComments.setText(downloadFailure1[0][11])
        self.test_browser.saveLocation.setText(downloadFailure1[1])
        self.test_browser.dropdowns[0].setCurrentIndex(downloadFailure1[0][2])
        self.test_browser.dropdowns[1].setCurrentIndex(downloadFailure1[0][3])
        self.test_browser.dropdowns[2].setCurrentIndex(downloadFailure1[0][4])
        self.test_browser.dropdowns[3].setCurrentIndex(downloadFailure1[0][5])
        self.assertTrue(self.test_browser.imageSearch())
        self.assertFalse(self.test_browser.imageDownload())

    def test_download_failure2(self):
        self.test_browser.lowerDate.setDate(downloadFailure2[0][0])
        self.test_browser.upperDate.setDate(downloadFailure2[0][1])
        self.test_browser.upperCount.setValue(downloadFailure2[0][7])
        self.test_browser.lowerCount.setValue(downloadFailure2[0][6])
        self.test_browser.lowerZoom.setValue(downloadFailure2[0][8])
        self.test_browser.upperZoom.setValue(downloadFailure2[0][9])
        self.test_browser.slideID.setText(downloadFailure2[0][10])
        self.test_browser.otherComments.setText(downloadFailure2[0][11])
        self.test_browser.saveLocation.setText(downloadFailure2[1])
        self.test_browser.dropdowns[0].setCurrentIndex(downloadFailure2[0][2])
        self.test_browser.dropdowns[1].setCurrentIndex(downloadFailure2[0][3])
        self.test_browser.dropdowns[2].setCurrentIndex(downloadFailure2[0][4])
        self.test_browser.dropdowns[3].setCurrentIndex(downloadFailure2[0][5])
        self.assertTrue(self.test_browser.imageSearch())
        self.assertFalse(self.test_browser.imageDownload())

    def test_download_failure3(self):
        self.test_browser.lowerDate.setDate(downloadFailure3[0][0])
        self.test_browser.upperDate.setDate(downloadFailure3[0][1])
        self.test_browser.upperCount.setValue(downloadFailure3[0][7])
        self.test_browser.lowerCount.setValue(downloadFailure3[0][6])
        self.test_browser.lowerZoom.setValue(downloadFailure3[0][8])
        self.test_browser.upperZoom.setValue(downloadFailure3[0][9])
        self.test_browser.slideID.setText(downloadFailure3[0][10])
        self.test_browser.otherComments.setText(downloadFailure3[0][11])
        self.test_browser.saveLocation.setText(downloadFailure3[1])
        self.test_browser.dropdowns[0].setCurrentIndex(downloadFailure3[0][2])
        self.test_browser.dropdowns[1].setCurrentIndex(downloadFailure3[0][3])
        self.test_browser.dropdowns[2].setCurrentIndex(downloadFailure3[0][4])
        self.test_browser.dropdowns[3].setCurrentIndex(downloadFailure3[0][5])
        self.assertTrue(self.test_browser.imageSearch())
        self.test_browser.imageDownload()
        self.assertFalse(self.test_browser.imageDownload())
        filePath = downloadSuccess[1] + '149'
        try:
            os.remove(filePath)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
   
