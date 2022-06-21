import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout
from PDFfunctions import splitFixed, splitCustom


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

        # Widgets definition
        numPages = QLabel(self)
        explanationMsg = QLabel('<h3>Split your PDF file in regular intervals</h3>', parent=self)
        numPages.setText('Pages interval: ')
        
        pagesInterval = QSpinBox()
        uploadButton = QtWidgets.QPushButton("Choose file")
        splitButton = QtWidgets.QPushButton("Split!")

        # Buttons functions
        uploadButton.clicked.connect(self.getFile)
        # showDialog('test')
        splitButton.clicked.connect(lambda: splitFixed(pagesInterval.value(), self.PDFfile))
        # splitButton.clicked.connect(lambda: showDialog('test'))
        


        
        # Add all widgets to layout
        layout.addWidget(uploadButton)
        layout.addWidget(explanationMsg)
        layout.addWidget(numPages)
        layout.addWidget(pagesInterval)
        layout.addWidget(splitButton)
        layout.addStretch()

    # Call outside functions
    @QtCore.pyqtSlot()
    def getFile(self):
        filePath, filters = QFileDialog.getOpenFileName(self, filter="*.pdf")
        setattr(self, 'PDFfile', filePath)


class customRange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(customRange, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        # Widgets definition
        uploadButton = QtWidgets.QPushButton("Choose file")
        explanationMsg = QLabel('<h3>Create a new file from a custom interval</h3>', parent=self)
        textInit = QLabel('From page:')
        textEnd = QLabel('to page:')
        splitButton = QtWidgets.QPushButton("Split!")
        initPage = QSpinBox()
        endPage = QSpinBox()

        # Add all widgets to horizontal layout
        hBox = QHBoxLayout()
        hBox.addWidget(textInit)
        hBox.addWidget(initPage)
        hBox.addWidget(textEnd)
        hBox.addWidget(endPage)
        hBox.addStretch()

        # Buttons functions
        uploadButton.clicked.connect(self.getFile)
        splitButton.clicked.connect(lambda: splitCustom(initPage.value(), endPage.value(), self.PDFfile))

        # Add all widgets to vertical layout
        layout.addWidget(uploadButton)
        layout.addWidget(explanationMsg)
        layout.addLayout(hBox)
        layout.addWidget(splitButton)
        layout.addStretch()
        
    @QtCore.pyqtSlot()
    def getFile(self):
        filePath, filters = QFileDialog.getOpenFileName(self, filter="*.pdf")
        setattr(self, 'PDFfile', filePath)



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


class customDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

    def addMessage(self, message):
        dMessage = QLabel(message)

        self.layout.addWidget(dMessage)
        self.setLayout(self.layout)
    
def showDialog(message):
    dialog = customDialog()
    dialog.addMessage(message)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())