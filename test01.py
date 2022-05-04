import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Exam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()
        
    def initUI(self):
        self.resize(1280, 900)
        self.setWindowTitle('Date')
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.show()
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self,'종료확인', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
        


        
app = QApplication(sys.argv)
w = Exam()
#ex = MyApp()
sys.exit(app.exec_())

    
