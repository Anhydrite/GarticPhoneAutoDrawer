import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from ui.mainWindow import Ui_MainWindow
from modules.autoDrawer import AutoDrawer
from modules.detectClicks import detectClick
import asyncio 


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setupButtons()
        self.drawer = AutoDrawer()  

    def setupButtons(self):
        self.drawSetup.clicked.connect(self.setupDrawArea)
        self.colorSetup.clicked.connect(self.setupColorArea)
        self.urlLoad.clicked.connect(self.setupImage)
        self.exitButton.clicked.connect(self.close)
        self.drawButton.clicked.connect(self.launchDraw)
       
    def setupDrawArea(self):
        self.drawStatus.setText("Configuration ...")
        self.drawStatus.setStyleSheet("color: orange;")
        start, end = detectClick()
        self.drawer.setupDrawArea(start, end)
        string = "Zone de dessin configurée x : {x}, y : {y}".format(x=start, y=end)
        self.drawStatus.setText(string)
        self.drawStatus.setStyleSheet("color: green;")
        self.launchComputing()

    def setupColorArea(self):
        self.colorAreaStatus.setText("Configuration ...")
        self.colorAreaStatus.setStyleSheet("color: orange;")
        start, end = detectClick()
        self.drawer.setupColorArea(start,end)
        string = "Zone des couleurs configurée x : {x}, y : {y} ".format(x=start, y=end)
        self.colorAreaStatus.setText(string)
        self.colorAreaStatus.setStyleSheet("color: green;")
        self.launchComputing()
        
    def setupImage(self):
        url = self.url.text()
        message = self.drawer.loadImage(url)
        self.statusLabel.setText(message[0])
        if(message[1] == 0):
            self.statusLabel.setStyleSheet("color: red;")
            return
        self.statusLabel.setStyleSheet("color: green;")
        self.launchComputing()
        
    def launchComputing(self):
        message = self.drawer.check()
        self.generalStatus.setText(message[0])
        if(message[1] != 1):
            return
        
        self.generalStatus.setText("Image en cours de traitement 1/2")
        message = self.drawer.computeImage()
        self.generalStatus.setText(message[0])   
        if(message[1] == 0):
            return
        self.generalStatus.setText(message[0])   
        message = self.drawer.updateColors()
        if(message[1] == 0):
             return
        self.generalStatus.setText(message[0])
        self.generalStatus.setStyleSheet("color: green;")


    def launchDraw(self):
        message = self.drawer.check()
        self.generalStatus.setText(message[0])
        if(message[1] != 3):
            return
        print("qdsqsd")
        self.drawer.newDraw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()    
    win.show()
    sys.exit(app.exec())