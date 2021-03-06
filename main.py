import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QMessageBox, QSpinBox
from PDFfunctions import splitFixed, splitCustom
from pathlib import Path


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window Settings
        self.setWindowTitle("PDF manager") # Window Title
        self.x, self.y, self.w, self.h = 0, 0, 325, 225
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.window = MainWindow(self)
        self.setCentralWidget(self.window)
        self.show()

class fixedRange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(fixedRange, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.PDFfile = None
        self.filename = ''

        # Widgets definition
        numPages = QLabel(self)
        explanationMsg = QLabel('<h3>Split your PDF file in regular intervals</h3>', parent=self)
        numPages.setText('Pages interval: ')
        
        self.pagesInterval = QSpinBox()
        uploadButton = QtWidgets.QPushButton("Choose file")
        splitButton = QtWidgets.QPushButton("Split!")
        self.filenameText = QLabel(self)

        # Buttons functions
        uploadButton.clicked.connect(self.getFile)

        splitButton.clicked.connect(self.splitFixed)

        # Add all widgets to layout
        layout.addWidget(self.filenameText)
        layout.addWidget(uploadButton)
        layout.addWidget(explanationMsg)
        layout.addWidget(numPages)
        layout.addWidget(self.pagesInterval)
        layout.addWidget(splitButton)
        layout.addStretch()
    
    def splitFixed(self):
        returnStatus = splitFixed(self.pagesInterval.value(), self.PDFfile)
        dialog = QMessageBox(self)
        dialog.setWindowTitle(" ")

        # TODO: fix it 
        if returnStatus == None:
            returnStatus = 'Successfully splitted!'

        dialog.setText(returnStatus)
        dialog.exec()

    @QtCore.pyqtSlot()
    def getFile(self):
        filePath, filters = QFileDialog.getOpenFileName(self, filter="*.pdf")
        setattr(self, 'PDFfile', filePath)
        setattr(self, 'filename', Path(filePath).stem + '.pdf')
        self.filenameText.setText('Selected: ' + self.filename)


class customRange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(customRange, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.PDFfile = None
        self.filename = ''

        # Widgets definition
        uploadButton = QtWidgets.QPushButton("Choose file")
        explanationMsg = QLabel('<h3>Create a new file from a custom interval</h3>', parent=self)
        textInit = QLabel('From page:')
        textEnd = QLabel('to page:')
        splitButton = QtWidgets.QPushButton("Split!")
        self.initPage = QSpinBox()
        self.endPage = QSpinBox()
        self.filenameText = QLabel(self)

        # Add all widgets to horizontal layout
        hBox = QHBoxLayout()
        hBox.addWidget(textInit)
        hBox.addWidget(self.initPage)
        hBox.addWidget(textEnd)
        hBox.addWidget(self.endPage)
        hBox.addStretch()

        # Buttons functions
        uploadButton.clicked.connect(self.getFile)
        splitButton.clicked.connect(self.splitCustom)

        # Add all widgets to vertical layout
        layout.addWidget(self.filenameText)
        layout.addWidget(uploadButton)
        layout.addWidget(explanationMsg)
        layout.addLayout(hBox)
        layout.addWidget(splitButton)
        layout.addStretch()
        
    def splitCustom(self):
        returnStatus = splitCustom(self.initPage.value(), self.endPage.value(), self.PDFfile)
        
        # TODO: fix it
        if returnStatus == None:
            returnStatus = 'Successfully splitted!'
        
        dialog = QMessageBox(self)
        dialog.setWindowTitle(" ")
        dialog.setText(returnStatus)
        dialog.exec()

    @QtCore.pyqtSlot()
    def getFile(self):
        filePath, filters = QFileDialog.getOpenFileName(self, filter="*.pdf")
        setattr(self, 'PDFfile', filePath)
        setattr(self, 'filename', Path(filePath).stem + '.pdf')
        self.filenameText.setText('Selected: ' + self.filename)


class MainWindow(QtWidgets.QWidget):        
    def __init__(self, parent):   
        super(MainWindow, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        tabHolder = QtWidgets.QTabWidget()
        tab1 = fixedRange()           
        tab2 = customRange()  

        # Add tabs
        tabHolder.addTab(tab1, "Split: fixed range") 
        tabHolder.addTab(tab2, "Split: custom range")  

        layout.addWidget(tabHolder)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())