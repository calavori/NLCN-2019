import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from attendList import AttendListMenu
from manage import ManageMenu
from face_detector import Face_detector
from data import Data

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = Data()
        self.dialogs = list()
        self.setWindowTitle('Menu')
        self.display()


    def display(self):
        layout = QVBoxLayout()

        label = QLabel('Ứng dụng điểm danh')
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)
        
        
        manageButton = QPushButton('Quản lý dữ liệu')
        manageButton.clicked.connect(lambda: self.openManage())

        attendListButton = QPushButton('Danh sách điểm danh')
        attendListButton.clicked.connect(lambda: self.openAttendList())
       
        rollCallButton = QPushButton('Điểm danh')
        rollCallButton.clicked.connect(lambda: self.openRollCall())

        widgets = [label, manageButton, attendListButton, rollCallButton]
        for w in widgets:
            layout.addWidget(w)
        
        widget = QWidget()
        widget.setLayout(layout)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(widget)
        

    def openAttendList(self):
        dialog = AttendListMenu()
        self.dialogs.append(dialog)
        dialog.show()

    def openManage(self):
        dialog = ManageMenu()
        self.dialogs.append(dialog)
        dialog.show()

    def openRollCall(self):
        face = Face_detector()
        id = face.detect()
        name = self.data.getDb_students_name(id[0])

        dialog = QMessageBox()
        dialog.setWindowTitle('Confirm')
        dialog.setText('Bạn có phải là '+ name + '-'+ id[0] + ' ?')
        dialog.setStandardButtons(QMessageBox.No|QMessageBox.Yes)
        yes = dialog.button(QMessageBox.Yes)
        yes.setText('Có')
        no = dialog.button(QMessageBox.No)
        no.setText('Không')
        
        respone = dialog.exec_()
        if respone == QMessageBox.Yes:
            self.data.addDb_attendance(id[0], id[1])
        if respone == QMessageBox.No:
            os.remove("dataset/attendance/" + id[1] + '.png')

