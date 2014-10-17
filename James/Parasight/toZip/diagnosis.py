from imagemanager import *
from desktopDiagnose import *
from loadingbar import *


# Diagnoser class. Emits a close signal to the main application when closed, and has signals
# connected to the diagnose thread class.
class Diagnoser(ImageManager):
    emitProgressUpdate = QtCore.pyqtSignal(int)
    submitSearch = QtCore.pyqtSignal(list)
    emitClose = QtCore.pyqtSignal()
    loadingBar = None

    def __init__(self):
        super(Diagnoser, self).__init__()
        # Set the style of the window (font size and type)
        #self.setStyleSheet('font-size: 11pt; font-family: Arial;')
        self.styleData = ''

        f = open('style', 'r')
        self.styleData = f.read()
        f.close()
        
        self.initUI()

    def initUI(self):
        #Creates the grid layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        
        #Add title
        titleLabel = QLabel(self)
        self.bannerImage = QtGui.QPixmap('images/MalariaDiagnosisTrans.png')
        self.bannerImageScaled = self.bannerImage.scaled(250, 60, Qt.KeepAspectRatio)
        titleLabel.setPixmap(self.bannerImageScaled)
        self.grid.addWidget(titleLabel, 0, 0, 1, 6, QtCore.Qt.AlignCenter)
        
        #Add widget to allow image to be uploaded from directory
        self.fileLine = QLineEdit(self)
        self.grid.addWidget(self.fileLine, 2, 1, 1, 3)
        self.grid.addWidget(self.createButton('Locate Image', self.findFile, 'Choose an image to be diagnosed'), 2, 4, 1, 1)

        #Upload button
        uploadBtn = self.createButton('Diagnose', self.diagnose, 'Submits the currently selected filepath')
        self.grid.addWidget(uploadBtn, 3, 1, 1, 4)

        #Add placeholder for image to be diagnosed
        self.label = QtGui.QLabel(self)
        self.mainImage = QtGui.QPixmap('images/logo.png')    
        self.label.setPixmap(self.mainImage.scaled(500, 500, Qt.KeepAspectRatio))
        self.label.setScaledContents(False)
        self.grid.addWidget(self.label, 4, 0, 1, 6, QtCore.Qt.AlignCenter)
    
        #Results display
        self.resultsLabel = QLabel('Press \'diagnose\' to test your image')
        self.resultsLabel.setStyleSheet('font-family: Verdana; font-size: 24px')

        self.grid.addWidget(self.resultsLabel, 5, 0, 1, 6, Qt.AlignCenter)

        self.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.setStyleSheet(self.styleData)
        self.setLayout(self.grid)
        self.move(300, 150)
        self.setWindowTitle('Parasight Image Diagnosis') #Title of the program
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(400, 300)
        self.show() 


    # Opens a file dialog to allow user to locate a file from the file system. Sets the text of the 
    # filename line to the file address, or displays the number of selected files if greater
    # than one
    def findFile(self):
        self.fileDialog = QFileDialog(self)
        filename = self.fileDialog.getOpenFileName()
        if filename == '':
            return
        if self.fileCheck(str(filename)) != True:
            self.warning('Attention', 'Invalid file type')
            return
        self.fileLine.setText(filename)
        self.changeImage(filename)
        

    # Displays a loading bar and submits the file path to the diagnose thread to handle running 
    # the diagnosis script. If the given file does not exist, return early. Otherwise, start the
    # diagnose thread.
    def diagnose(self):
        self.loadingBar = WaitingBar(0)
        self.loadingBar.show()

        if self.fileLine.text() == '':
            self.loadingBar.deleteLater()
            self.loadingBar = None
            self.warning('Attention', 'Invalid file type')
            return
        filename = str(self.fileLine.text())
        self.diagnoseThread = DiagnoseThread(filename)
        self.connect(self.diagnoseThread, self.diagnoseThread.emitResults, self.displayResults)
        self.diagnoseThread.start()
        
    # Function that is called once the diagnose thread is complete. The function is passed the
    # results from the diagnose thread: the filepath of the results and whether the image is infected
    # or not.
    def displayResults(self, returnedResults):
        # Delete the loading bar
        self.loadingBar.deleteLater()
        self.loadingBar = None
        
        filepath = returnedResults[0]
        result = returnedResults[1]
        
        # Show the returned, grided image
        self.changeImage(filepath)
        tmp = self.grid.itemAt(5)
        
        # Change the result label at the bottom of the window
        if tmp is not None:
            widget = tmp.widget()
            if widget is not None:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        if result:
            self.resultsLabel = QLabel('Potential infection')
            self.resultsLabel.setStyleSheet('font-family: Verdana; font-size: 24px; color: #E74c3c')
        else:
            self.resultsLabel = QLabel('No parasite detected')
            self.resultsLabel.setStyleSheet('font-family: Verdana; font-size: 24px; color: #056927')
        self.grid.addWidget(self.resultsLabel, 5, 0, 1, 6, Qt.AlignCenter)   
        self.show()
        print result
        
        return

    #Changes the displayed image to the passed filename
    def changeImage(self, filename):
        newImage = QtGui.QPixmap(filename)
        
        imageSize = newImage.size()
        if imageSize.height() > 1000:
            newImage = newImage.scaled(1000, 1000, Qt.KeepAspectRatio)
        self.label.setPixmap(newImage)
       
        self.show()

    # Checks the provided file path against the allowable file types in lists.py
    def fileCheck(self, path):
        if path == '':
            return False
        for filetype in FILE_TYPES:
            if path.endswith(filetype):
                return True
        return False      


# Separate class to handle running the diagnose script. This creates an instance of the
# Paramiko class, which then runs the diagnose script. This is passed a given image file
# path and is returned a labelled image and the result of the diagnosis.
class DiagnoseThread(QtCore.QThread):
    emitResults = QtCore.SIGNAL("signal")

    def __init__(self, filepath):
        QtCore.QThread.__init__(self)
        self.diagnoser = Paramiko()
        self.myfilepath = filepath

    def run(self):
        returnPath, result = self.diagnoser.Query(self.myfilepath)
        allResults = (returnPath, result)
        self.emit(self.emitResults, allResults)
