import sys
import os
import io
from PIL import Image
import time
import cPickle as p
from lists import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from database import *
import base64

MAX_COMMENT_LEN = 100




class ImageBrowser(QtGui.QDialog):
    
    def __init__(self):
        super(ImageBrowser, self).__init__()
        self.viewer = ImageViewer()
        self.initUI()
        self.results = []
        self.database = Database()
        
    def initUI(self):
        resultsWidth = 24
        self.dropdowns = []
        l = 0

        #Get label names for the search bar
        labelNames = []
        for name in FIELD_NAMES:
            labelNames.append(QLabel(name))

        #Creates a list of dropdown menus
        for i in range (0, 4):
            self.dropdowns.append(QComboBox(self))
            for option in ALL_FIELDS[i]:
                self.dropdowns[i].addItem(option)

        #Create grid layout
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
       
        
        #Title - do we want to use an image?
        titleLabel = QLabel('Malaria Image Browser')
        self.grid.addWidget(titleLabel, l, 0, 1, 30, QtCore.Qt.AlignCenter)
        l+=1
        self.grid.addWidget(QLabel('Results'), l, 0, 1, resultsWidth, QtCore.Qt.AlignCenter)
        self.grid.addWidget(QLabel('Search Options'), l, resultsWidth, 1, 6, QtCore.Qt.AlignCenter)
        l+=1

        #Housekeeping for results viewer section
        self.grid.addWidget(self.viewer, l, 0, 16, resultsWidth)


        #Add date searching option
        self.grid.addWidget(QLabel('Date'), l, resultsWidth)
        self.grid.addWidget(QLabel('From'), l, resultsWidth+2, QtCore.Qt.AlignCenter)
        self.grid.addWidget(QLabel('To'), l, resultsWidth+4, QtCore.Qt.AlignCenter)
        l+=1

        self.lowerDate = QDateEdit()
        self.upperDate = QDateEdit()
        self.lowerDate.setDisplayFormat("dd-MM-yyyy")
        self.upperDate.setDisplayFormat("dd-MM-yyyy")
        self.lowerDate.setMinimumDate(QDate(2013, 1, 1))
        self.upperDate.setMinimumDate(QDate(2013, 1, 1))
        self.lowerDate.setMaximumDate(QDate.currentDate())
        self.upperDate.setMaximumDate(QDate.currentDate())
        self.upperDate.setDate(self.upperDate.maximumDate())
        self.lowerDate.setDate(self.lowerDate.minimumDate())
        self.grid.addWidget(self.lowerDate, l, resultsWidth+2, 1, 2)
        self.grid.addWidget(self.upperDate, l, resultsWidth+4, 1, 2)
        l+=1
        j = 0
        
        for name in labelNames:
        #Add label to line
            self.grid.addWidget(labelNames[j], l, resultsWidth, 1, 2)
            #For first 4 labels, add dropdown menus
            if j < 4:
                self.grid.addWidget(self.dropdowns[j], l, resultsWidth+2, 1, 4)
            #Then add the count input
            elif j == 4:
                self.grid.addWidget(QLabel('Range'), l, resultsWidth+2, 1, 4, QtCore.Qt.AlignCenter)
                l+=1
                self.lowerCount = QDoubleSpinBox()
                self.upperCount = QDoubleSpinBox()
                self.lowerCount.setRange(0, 1)
                self.upperCount.setRange(0, 1)
                self.lowerCount.setDecimals(3)
                self.upperCount.setDecimals(3)
                self.lowerCount.setSingleStep(0.001)
                self.upperCount.setSingleStep(0.001)
                self.upperCount.setValue(self.upperCount.maximum())
                self.grid.addWidget(self.lowerCount, l, resultsWidth+2, 1, 2)
                self.grid.addWidget(self.upperCount, l, resultsWidth+4, 1, 2)
            #Zoom input
            elif j == 5:
                self.grid.addWidget(QLabel('Range'), l, resultsWidth+2, 1, 4, QtCore.Qt.AlignCenter)
                l+=1
                self.lowerZoom = QSpinBox()
                self.upperZoom = QSpinBox()
                self.lowerZoom.setRange(0, 1000000)
                self.upperZoom.setRange(0, 1000000)
                self.upperZoom.setValue(self.upperZoom.maximum())
                self.grid.addWidget(self.lowerZoom, l, resultsWidth+2, 1, 2)
                self.grid.addWidget(self.upperZoom, l, resultsWidth+4, 1, 2)
            #Allow custom slide ID
            elif j == 6:
                self.slideID = QLineEdit()
                self.slideID.setMaxLength(25)
                self.grid.addWidget(self.slideID, l, resultsWidth+2, 1, 4)
            #Allow user to add additional comments
            elif j == 7:
                self.otherComments = QTextEdit()
                self.grid.addWidget(self.otherComments, l, resultsWidth+2, 1, 4)

            j = j + 1
            l = l + 1

        self.searchButton = self.createButton('Search', self.imageSearch, toolTip[j])
        self.grid.addWidget(self.searchButton, l, resultsWidth, 1, 3)  
        self.resetButton = self.createButton('Reset', self.resetFields, toolTip[j])
        self.grid.addWidget(self.resetButton, l, resultsWidth+3, 1, 3)    
        l+=1
        self.saveLocation = QLineEdit(self)
        self.saveLocation.setText('<Download Location>')
        self.grid.addWidget(self.saveLocation, l, resultsWidth, 1, 3)  
        self.grid.addWidget(self.createButton('Locate', self.findFile, toolTip[0]), l, resultsWidth+3, 1, 3)
        l+=1
        self.grid.addWidget(self.createButton('Download', self.imageDownload, toolTip[j]), l, resultsWidth, 1, 6)    
    

        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Parasight Image Browser') #Title of the program
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1500, 800)
#        self.showMaximized()
        self.show() 

    def createButton(self, name, buttonFunction, tooltip):
        btn = QPushButton(name, self)
        btn.clicked.connect(buttonFunction)
        btn.setToolTip(tooltip)
        return btn

    def warning(self, title, text):
        return QMessageBox.warning(self, title, text, QMessageBox.Ok)

    def resetFields(self):
        self.lowerDate.setDate(self.lowerDate.minimumDate())
        self.upperDate.setDate(self.upperDate.maximumDate())
        for field in self.dropdowns:
            field.setCurrentIndex(0)
        self.lowerCount.setValue(0)
        self.upperCount.setValue(self.upperCount.maximum())
        self.lowerZoom.setValue(0)
        self.upperZoom.setValue(self.upperZoom.maximum())
        self.slideID.clear()
        self.otherComments.clear()
        self.viewer.clearLayout()
        self.saveLocation.setText('<Download Location>')

    def imageSearch(self):
        labels = ["NULL" for x in range(0, 9)]
        i = 0

        lowDate = QDate.toString(self.lowerDate.date(), "dd-MM-yyyy")
        upDate = QDate.toString(self.upperDate.date(), "dd-MM-yyyy")
        dateRange = lowDate + ';' + upDate
        parasiticCount = str(self.lowerCount.value()) + ';' + str(self.upperCount.value())
        zoomRange = str(self.lowerZoom.value()) + ';' + str(self.upperZoom.value())
      
        if lowDate != upDate:
            labels[i] = str(dateRange)
        i+=1

        comment = self.otherComments.toPlainText()
        #Check that given comment is not too long
        if len(comment) > MAX_COMMENT_LEN:
            #self.warning('Attention', 'Please limit comment length to ' + `MAX_COMMENT_LEN` + ' words')
            return False

    
        for field in self.dropdowns:
            if str(field.currentText()) != '<Please select one>':
                labels[i] = str(field.currentText())
            i += 1
        
        labels[i] = str(parasiticCount)
        i+=1
        labels[i] = str(zoomRange)
        i+=1
        if self.slideID.text() != '':
            labels[i] = str(self.slideID.text())
        i+=1
        if comment != '':
            labels[i] = str(comment)
        i+=1

        self.results, warning = self.database.query_create(labels)
        if warning != "Success":
            #self.warning('Uh oh!', warning)
            return False
        self.viewer.displayImages(self.results)
        return True

    def imageDownload(self):
        save_directory = self.saveLocation.text() + '/'
        if not QFile.exists(save_directory):
           # self.warning('Warning!', 'Specified directory path does not exist')
            return False
        for result in self.results:
            save_location = save_directory + `result[0]`        
            if QFile.exists(save_location):
                return False
                #self.warning('Warning!', 'Specified file path already exists!')            
            with open(save_location, "wb") as image:
                image.write(base64.decodestring(result[-1]))
                image.close()
        return True
        #im = Image.open(io.BytesIO(bytes))
#im.save("test.jpg")
    def findFile(self):
        self.fileDialog = QFileDialog(self)
        filename = self.fileDialog.getExistingDirectory(self, "Select Directory")
        self.saveLocation.setText(filename)
    
  
        
class ImageViewer(QtGui.QListView):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.initUI()
        
    def initUI(self):
        #Create grid layout
        self.imageGrid = QtGui.QGridLayout()
        self.imageGrid.setSpacing(10)
        self.model = QStandardItemModel(self)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(100, 100))
        

    def displayImages(self, results):
        self.clearLayout()
        #print 'Displaying images'
        for i in range(0, len(results)):
            self.model.appendRow(self.showImage(results[i][-1], results[i][0]))
        self.setModel(self.model)
        self.show()
        
       

    def showImage(self, bytes, image_label):
        image_bytes = base64.b64decode(bytes)
        label = QtGui.QLabel(self)
        qimg = QtGui.QPixmap()
        qimg.loadFromData(image_bytes)
        qimgScaled = qimg.scaled(300, 300)
        label.setPixmap(qimgScaled)
        label.setScaledContents(True)
        icon = QIcon(qimgScaled)
        return QStandardItem(icon, str(image_label))

                  
    def clearLayout(self):
        self.model.clear()
       
