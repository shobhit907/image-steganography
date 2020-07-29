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
        self.encOpenImageButton.clicked.connect(self.encOpenBackImage)
        self.encButton.clicked.connect(self.encrypt)
        self.encSaveButton.clicked.connect(self.saveEncImage)
        self.decOpenImageButton.clicked.connect(self.decOpenImage)
        self.decButton.clicked.connect(self.decrypt)
        self.decSaveButton.clicked.connect(self.saveDecOutput)
        self.encImage=None
        self.encImageOutput=None
        self.decImage=None
        
    def encOpenTextFile(self):
        filename=QFileDialog.getOpenFileName(self,caption="Select text file to be hidden",directory=".",filter="Text files (*.txt *.odt *.doc *.docx)")
        if(filename[0]):
            f = open(filename[0], 'r')
            with f:
                data = f.read()
                self.encInputFile.setPlainText(data)
    
    def encOpenBackImage(self):
        filename=QFileDialog.getOpenFileName(self,caption="Select Image in which to encrypt",directory=".",filter="Images (*.png *.jpg *.jpeg)")[0]
        if(filename):
            frameGeometry=self.encBackImageFrame.geometry()
            frameWidth=frameGeometry.width()
            frameHeight=frameGeometry.height()
            self.encImage=cv2.imread(filename)
            self.pixmap=QPixmap(filename)
            self.pixmap=self.pixmap.scaled(frameWidth,frameHeight,QtCore.Qt.KeepAspectRatio)
            self.encImageLabel.setPixmap(self.pixmap)
            
    def encrypt(self):
        msg=self.encInputFile.toPlainText()
        if self.encImage is None:
            return
        self.encImageOutput=Steganography.encrypt(msg,self.encImage)
        print("Done")
        qimage=QtGui.QImage(self.encImageOutput.data,self.encImageOutput.shape[1],self.encImageOutput.shape[0],self.encImageOutput.strides[0],QtGui.QImage.Format_RGB888).rgbSwapped()
        self.pixmap=QtGui.QPixmap.fromImage(qimage)
        frameGeometry=self.encOutputFrame.geometry()
        frameWidth=frameGeometry.width()
        frameHeight=frameGeometry.height()
        self.pixmap=self.pixmap.scaled(frameWidth,frameHeight,QtCore.Qt.KeepAspectRatio)
        self.encOutputImageLabel.setPixmap(self.pixmap)

    def saveEncImage(self):
        if self.encImageOutput is None:
            return
        filename=QFileDialog.getSaveFileName(self,caption="Save Encrypted Output Image File",directory="output.png",filter="Images (*.png *.jpg *.jpeg)")[0]
        if(filename):
            # print(filename)
            cv2.imwrite(filename,self.encImageOutput,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])
            # cv2.imwrite(filename,self.encImageOutput,[int(cv2.IMWRITE_JPEG_QUALITY), 90])
            # cv2.imwrite(filename,self.encImageOutput)

    def decOpenImage(self):
        filename=QFileDialog.getOpenFileName(self,caption="Select Image to decrypt",directory=".",filter="Images (*.png *.jpg *.jpeg)")[0]
        if(filename):
            frameGeometry=self.decInputImageFrame.geometry()
            frameWidth=frameGeometry.width()
            frameHeight=frameGeometry.height()
            self.decImage=cv2.imread(filename)
            self.pixmap=QPixmap(filename)
            self.pixmap=self.pixmap.scaled(frameWidth,frameHeight,QtCore.Qt.KeepAspectRatio)
            self.decInputImageLabel.setPixmap(self.pixmap)

    def decrypt(self):
        if self.decImage is None:
            return
        msg=Steganography.decrypt(self.decImage)
        print("Done")
        self.decOutput.setPlainText(msg)

    def saveDecOutput(self):
        msg=self.decOutput.toPlainText()
        if msg is None or len(msg)==0:
            return
        filename=QFileDialog.getSaveFileName(self,caption="Save file as",directory="output.txt",filter="Text files (*.txt *.odt *.doc *.docx)")[0]
        if(filename):
            with open(filename,'w') as f:
                f.write(msg)




app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()