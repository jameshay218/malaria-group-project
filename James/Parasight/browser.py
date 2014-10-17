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
import thread
import csv
from imagemanager import *
from loadingbar import *


MAX_COMMENT_LEN = 100


class ImageBrowser(ImageManager):
    # Connects the close signal to the owner application, and the submit search button to the
    # loading bar
    submitSearch = QtCore.pyqtSignal(list)
    emitClose = QtCore.pyqtSignal()
    allResultsDict = {}

    def __init__(self):
        super(ImageBrowser, self).__init__()
        self.viewer = ImageViewer()
        self.styleData = ''

        f = open('style', 'r')
        self.styleData = f.read()
        f.close()
        self.initUI()
        self.results = []
        
    # Initialises the user interface
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
       
        
        #Title - do we want to use an image as a banner instead?
        titleLabel = QLabel(self)
        self.bannerImage = QtGui.QPixmap('images/ImageBrowserTrans.png')
        self.bannerImageScaled = self.bannerImage.scaled(250, 60, Qt.KeepAspectRatio)
        titleLabel.setPixmap(self.bannerImageScaled)
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
        
        # Go through all of the provided input labels and add different line edits accordingly
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

        # Add functional buttons to the interface
        self.grid.addWidget(self.createButton('Search', self.imageSearch, 'Searches the database with the currently selected labels'), l, resultsWidth, 1, 3)    
        self.grid.addWidget(self.createButton('Reset', self.resetFields, 'Resets all fields'), l, resultsWidth+3, 1, 3)    
        l+=1
        self.saveLocation = QLineEdit(self)
        self.saveLocation.setText('<Download Location>')
        self.grid.addWidget(self.saveLocation, l, resultsWidth, 1, 3)  
        self.grid.addWidget(self.createButton('Locate', self.findFile, 'Choose a directory to save results'), l, resultsWidth+3, 1, 3)
        l+=1
        self.grid.addWidget(self.createButton('Download', self.imageDownload, 'Downloads the current search results'), l, resultsWidth, 1, 6)    
    

        # Final housekeeping to display the window
        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Parasight Image Browser') #Title of the program
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(1500, 800)
        self.show() 
 
    # Resets all optional line edits and dropdown selections 
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

    # Passes a list of search criteria to the database interface class which returns a list of 
    # search results and accompanying byte arrays
    def imageSearch(self):
        # Create a separate loading bar
        self.loadingBar = WaitingBar(0)
        self.loadingBar.show()
        
        #Create a list of null labels
        labels = ["NULL" for x in range(0, 9)]
        i = 0

        # Get's the date, count and zoom ranges for the search
        lowDate = QDate.toString(self.lowerDate.date(), "dd-MM-yyyy")
        upDate = QDate.toString(self.upperDate.date(), "dd-MM-yyyy")
        dateRange = lowDate + ';' + upDate
        parasiticCount = str(self.lowerCount.value()) + ';' + str(self.upperCount.value())
        zoomRange = str(self.lowerZoom.value()) + ';' + str(self.upperZoom.value())
      
        if lowDate != upDate:
            labels[i] = str(dateRange)
        i+=1

        # Get the comment search criteria
        comment = self.otherComments.toPlainText()

        #Check that given comment is not too long
        if len(comment) > MAX_COMMENT_LEN:
            self.warning('Attention', 'Please limit comment length to ' + `MAX_COMMENT_LEN` + ' words')
            return

        # Get the remaining search criteria
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
       
        # Once all labels taken from the editable fields and stored in label, a new thread is
        # created to handle submitting the query to the database. This prevents the entire window
        # from freezing until the submission is complete.
        self.searchThread = SearchThread(labels)
        self.connect(self.searchThread, self.searchThread.emitResults, self.displayResults)
        self.searchThread.start()
                  

    # Captures the returned results from the search thread. Deletes the loading bar and stores
    # these results to be added to the image viewer.
    def displayResults(self, returnedResults):
        self.loadingBar.deleteLater()
        self.loadingBar = None
        self.results = returnedResults[0]
        for result in self.results:
            self.allResultsDict[str(result[0])] = result
        self.warningText = returnedResults[1]
        # If the query did not return successful, display the warning message
        if self.warningText != "Success":
            self.warning('Uh oh!', self.warningText)
        self.viewer.displayImages(self.results, self.allResultsDict)
           

    # Saves the currently stored image and label results to a directory specified on the window.
    # Stores all images, and all accompanying labels as a .csv file.
    def imageDownload(self):
        # Checks if results are empty
        if self.results == []:
            self.warning('Warning!', 'No results to download!')
            return False

        # Checks if directory has not been specified
        if self.saveLocation.text() == '<Download Location>':
            self.warning('Warning!', 'Specified directory path does not exist')
            return False
        save_directory = self.saveLocation.text() + '/'
        saveResults = [['Index', 'Laboratory', 'Diagnosis', 'Host species', 'Parasite strain', 'Parasitic count', 'Zoom', 'Additional Slide ID', 'Other Comments', 'Date added']]
        csvFileName = save_directory + str(self.results[0][9]) + '.csv'
        #print csvFileName

        # Checks that the given directory exists
        if not QFile.exists(save_directory):
            self.warning('Warning!', 'Specified directory path does not exist')
            return False

        # Makes sure that the function is not overwriting a previous .csv file
        if QFile.exists(csvFileName):
            fileWarning = 'A .csv file of the name ' + csvFileName + ' already exists! Please rename the existing file before saving'
            #print fileWarning
            self.warning('Warning!', fileWarning)
            return False

        # Makes sure that no images are being overwritten
        for result in self.results:
            save_location = save_directory + `result[0]`        
            if QFile.exists(save_location):
                imageWarning = save_location + ' already exists! Please rename the existing file before saving'
                self.warning('Warning!', `imageWarning`)
                return False

        # Goes through the results list and saves each image to the directory specified above
        for result in self.results:
            toBeSaved = []
            for i in range(0, 10):
                toBeSaved.append(str(result[i]))
            saveResults.append(toBeSaved)
            save_location = save_directory + `result[0]`        
            with open(save_location, "wb") as image:
                image.write(base64.decodestring(result[-1]))
                image.close()
        # Saves the .csv file of labels
        self.saveCSV(csvFileName, saveResults)
       
    # Function to open the file location and save the given results there
    def saveCSV(self, saveLocation, saveResults):
        with open(saveLocation, "wb") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(saveResults)
          
    # Allows user to locate a filepath from their file system
    def findFile(self):
        self.fileDialog = QFileDialog(self)
        filename = self.fileDialog.getExistingDirectory(self, "Select Directory")
        self.saveLocation.setText(filename)
    
  
# Separate class to handle displaying the returned images.        
class ImageViewer(QtGui.QListView):
    currentResultsDict = {}
    currentImage = None
    currentIndex = ''

    def __init__(self):
        super(ImageViewer, self).__init__()
        self.styleData = ''

        f = open('style', 'r')
        self.styleData = f.read()
        f.close()
        self.initUI()
        
    def initUI(self):
        #Create grid layout
        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.imageGrid = QtGui.QGridLayout()
        self.imageGrid.setSpacing(10)
        self.model = QStandardItemModel(self)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(100, 100))
        self.doubleClicked.connect(self.test)
        
    # Clears the current layout and adds each image to the view in turn
    def displayImages(self, results, givenResultsDict):
        self.currentResultsDict = givenResultsDict
        self.clearLayout()
        for i in range(0, len(results)):
            addedItem = self.showImage(results[i][-1], results[i][0])
            self.model.appendRow(addedItem)
        self.setModel(self.model)
        self.show()
       
    # Changes the displayed individual image, changing the table of labels and the image displayed
    def changeSingleImage(self, selectedIndex):
             
        # Change labels
        self.tableView.setItem(0, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][0])))
        self.tableView.setItem(1, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][1])))
        self.tableView.setItem(2, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][2])))
        self.tableView.setItem(3, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][3])))
        self.tableView.setItem(4, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][4])))
        self.tableView.setItem(5, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][5])))
        self.tableView.setItem(6, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][6])))
        self.tableView.setItem(7, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][7])))
        self.tableView.setItem(8, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][8])))
        self.tableView.setItem(9, 1, QTableWidgetItem(str(self.currentResultsDict[selectedIndex][9])))

        # Convert the given byte array to an image and display it
        image_bytes = base64.b64decode(self.currentResultsDict[selectedIndex][11])
        pictureLabel = QtGui.QLabel(self)
        qimg = QtGui.QPixmap()
        qimg.loadFromData(image_bytes)
        
        # Checks the image size. If too big, scales the image so that it fits on the screen
        imageSize = qimg.size()
        if imageSize.height() > 900:
            qimg = qimg.scaled(900, 900, Qt.KeepAspectRatio)
        pictureLabel.setPixmap(qimg)
        self.currentImage.grid.addWidget(pictureLabel, 0, 1, 20, 1,  QtCore.Qt.AlignCenter | Qt.AlignTop)

    # Opens a pop out window, displaying the image and labels corresponding to a given index
    def showSingleImage(self, selectedIndex):
        rowNumber = 0
        headingLabels = []
        
        #Create a new widget to display the individual image
        self.currentImage = QtGui.QDialog()
        self.currentImage.grid = QtGui.QGridLayout()
        self.currentImage.grid.setSpacing(10)
        self.currentImage.grid.setColumnMinimumWidth(0, 350)
        
        # Set the style of the window
        self.currentImage.styleData = ''

        f = open('style', 'r')
        self.currentImage.styleData = f.read()
        f.close()
       
        # Create a table to display the accompanying labels
        self.tableView = QtGui.QTableWidget()
        self.tableView.setRowCount(10)
        self.tableView.setColumnCount(2)

        # Add headings
        self.tableView.setItem(0, 0, QTableWidgetItem('Image index:'))
        self.tableView.setItem(1, 0, QTableWidgetItem('Source laboratory:'))
        self.tableView.setItem(2, 0, QTableWidgetItem('Diagnosis:'))
        self.tableView.setItem(3, 0, QTableWidgetItem('Host species:'))
        self.tableView.setItem(4, 0, QTableWidgetItem('Parasite strain:'))
        self.tableView.setItem(5, 0, QTableWidgetItem('Parasitic count:'))
        self.tableView.setItem(6, 0, QTableWidgetItem('Zoom:'))
        self.tableView.setItem(7, 0, QTableWidgetItem('Additional Slide ID:'))
        self.tableView.setItem(8, 0, QTableWidgetItem('Other comments:'))
        self.tableView.setItem(9, 0, QTableWidgetItem('Date added:'))

        # Hide the cell indices
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setShowGrid(False)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 180)

        # Make table not editable
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.currentImage.grid.addWidget(self.tableView, 0, 0, 15, 1)
        # Display the given image
        self.changeSingleImage(selectedIndex)
            
        # Window housekeeping
        self.currentImage.setLayout(self.currentImage.grid)
        self.currentImage.move(300, 150)
        self.currentImage.setWindowTitle(str(self.currentResultsDict[selectedIndex][0])) #Title of the program
        self.currentImage.setWindowIcon(QIcon('images/logo.png'))
        self.currentImage.setStyleSheet(self.currentImage.styleData)
        self.currentImage.resize(600, 600)
        self.currentImage.show() 

    # Connects the display of a single image to double clicking an icon in the list view
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def test(self, index):
        selectedIndex = str(index.data().toString())
        self.showSingleImage(selectedIndex)
   
    # Creates an icon from the given image label to add to the list view
    def showImage(self, bytes, image_label):
        image_bytes = base64.b64decode(bytes)
        label = QtGui.QLabel(self)
        qimg = QtGui.QPixmap()
        qimg.loadFromData(image_bytes)
        qimgScaled = qimg.scaled(300, 300)
        label.setPixmap(qimgScaled)
        label.setScaledContents(True)
        icon = QIcon(qimgScaled)
        item = QStandardItem(icon, str(image_label))
        item.setDragEnabled(False)
        item.setEditable(False)
        return item

    # Clears the layout of all images
    def clearLayout(self):
        self.currentImage = None
        self.model.clear()
       



# Separate helper class to handle the SQL search query. Creates an instance of the database class
# (thereby connecting to the database). Signals to the browser class once done with the returned
# results
class SearchThread(QtCore.QThread):
    emitResults = QtCore.SIGNAL("signal")

    def __init__(self, labels):
        QtCore.QThread.__init__(self)
        self.database = Database()
        self.mylabels = labels

    def run(self):
        results, warning = self.database.query_create(self.mylabels)
        allResults = (results, warning)
        self.emit(self.emitResults, allResults)
       
