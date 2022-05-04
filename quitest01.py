import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import QDateTime, Qt, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap
from time import sleep


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.dateTime = QDateTime.currentDateTime()
        self.initUI()

    def initUI(self):
       # self.setWindowIcon(QIcon('./Project/logo.png'))
        self.statusBar().showMessage(self.dateTime.toString(Qt.DefaultLocaleShortDate))

        self.setWindowTitle('Project')
       # self.resize(1280,680)
       # self.center()
        self.showMaximized()

   # def Video_to_frame(self)
   #     mjpg_PATH = "http://localhost:9090/?action=stream"
   #     cap = cv2.VideoCapture(mjpg_PATH)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
