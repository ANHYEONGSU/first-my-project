import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from time import sleep
from Module import sock_cli, temper
import threading


class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ForSign")
        MainWindow.showMaximized()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.video_viewer_label = QtWidgets.QLabel(self.centralwidget)
        self.video_viewer_label.setGeometry(QtCore.QRect(10, 10, 900, 640))

        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        #self.data = QDate.currentDate()
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusBar.showMessage(self.date.toString(Qt.DefaultLocaleShortDate))
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self,'종료확인', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


    def Video_to_frame(self, MainWindow):
        mjpg_PATH = "http://localhost:9090/?action=stream"
        cap = cv2.VideoCapture(mjpg_PATH)

        while True:
            self.ret, self.frame = cap.read()
            if self.ret:
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(900, 640, QtCore.Qt.IgnoreAspectRatio)
                self.video_viewer_label.setPixmap(self.p)
                self.video_viewer_label.update()             
                sleep(0.01)            
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def check_temp(self):
        #global running
        #global r_flag
        global cli
        global msg
        label2.resize(300,200)
        temp = '0'
        #while running:
        while True:
            sign = cli.recmessage()
            #sign = '0'
            #r_flag = sign

            #print("sign= ",sign)

            if '0' in sign:
                label2.setText("체온을 측정합니다. 잠시만 기다려주세요.   측정온도: " + temp)
                label2.setStyleSheet("color: red;"
                             "border-style: solid;"
                             "border-width: 5px;"
                             "border-color: #FA8072;"
                             "border-radius: 5px")

                speak(option,msg[0])
                tot_temp = 0.0
                for i in range(3):
                    #dis = a.distance()
                    temper = a.get_temp()
                    tot_temp += temper
                temper = round(tot_temp / 3.0, 2)
                temp = str(temper)
                cli.sendtemp(temp)

                #print(temp)
                print("온도 보냄   " + temp)

            elif '1' in sign:
                label2.setText("등록자 / 온도정상")
                label2.setStyleSheet("color: green;"
                            "border-style: solid;"
                            "border-width: 5px;"
                            "border-color: #7FFFD4;"
                            "border-radius: 5px")
                print("등록자 / 온도정상")
                speak(option,msg[1])

            elif '2' in sign:
                label2.setText("등록자 / 온도이상")
                label2.setStyleSheet("color: blue;"
                            "border-style: solid;"
                            "border-width: 5px;"
                            "border-color: #1E90FF;"
                            "border-radius: 5px")
                print("등록자 / 온도이상")
                speak(option,msg[2])

            elif '3' in sign:
                label2.setText("미등록자 / 온도정상")
                label2.setStyleSheet("color: blue;"
                            "border-style: solid;"
                            "border-width: 5px;"
                            "border-color: #1E90FF;"
                            "border-radius: 5px")
                print("미등록자 / 온도정상")
                speak(option,msg[3])

            elif '4' in sign:
                label2.setText("미등록자 / 온도이상")
                label2.setStyleSheet("color: blue;"
                            "border-style: solid;"
                            "border-width: 5px;"
                            "border-color: #1E90FF;"
                            "border-radius: 5px")
                print("미등록자 / 온도이상")
                speak(option,msg[4])

            else:
                pass

            #print("36.5도 정상입니다.")
            time.sleep(0.1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ProjectsB", "ProjectsB"))

    # video_to_frame
    def video_thread(self, MainWindow):
        thread = threading.Thread(target=self.Video_to_frame, args=(self,))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)

    ui.video_thread(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())


