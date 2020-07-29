import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog,QLabel
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from ImageSteganography import Steganography


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("img-stg.ui", self)
        self.encOpenFile.clicked.connect(self.encOpenTextFile)
        self.encOpenImage.clicked.connect(self.encOpenBackImage)
        self.encButton.clicked.connect(self.encrypt)
        self.filename=""

    def encOpenTextFile(self):
        filename=QFileDialog.getOpenFileName(self,caption="Select text file to be hidden",directory=".",filter="Text files (*.txt *.odt *.doc *.docx)")
        if(filename[0]):
            f = open(filename[0], 'r')
            with f:
                data = f.read()
                self.encInputFile.setPlainText(data)
    
    def encOpenBackImage(self):
        self.filename=QFileDialog.getOpenFileName(self,caption="Select text file to be hidden",directory=".",filter="Images (*.png *.jpg *.jpeg)")[0]
        print(self.filename)
        if(self.filename):
            frameGeometry=self.encBackImageFrame.geometry()
            frameWidth=frameGeometry.width()
            frameHeight=frameGeometry.height()
            print(frameWidth,frameHeight)
            self.pixmap=QPixmap(self.filename)
            self.pixmap=self.pixmap.scaled(frameWidth,frameHeight,QtCore.Qt.KeepAspectRatio)
            print(self.pixmap.height())
            self.encImageLabel.setPixmap(self.pixmap)
            
    def encrypt(self):
        msg=self.encInputFile.toPlainText()
        print(msg)
        print(self.filename)
        img=cv2.imread(self.filename)
        img=Steganography.encrypt(msg,img)
        print("Done")
        print(img.strides)
        qimage=QtGui.QImage(img.data,img.shape[1],img.shape[0],img.strides[0],QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap=QtGui.QPixmap.fromImage(qimage)
        frameGeometry=self.encOutputFrame.geometry()
        frameWidth=frameGeometry.width()
        frameHeight=frameGeometry.height()
        self.pixmap=self.pixmap.scaled(frameWidth,frameHeight,QtCore.Qt.KeepAspectRatio)
        self.encOutputImageLabel.setPixmap(self.pixmap)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()