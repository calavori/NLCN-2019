import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from attendList import AttendListMenu

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
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

        attendListButton = QPushButton('Danh sách điểm danh')
        attendListButton.clicked.connect(lambda: self.openAttendList(attendListButton))
       
        rollCallButton = QPushButton('Điểm danh')

        widgets = [label, manageButton, attendListButton, rollCallButton]
        for w in widgets:
            layout.addWidget(w)
        
        widget = QWidget()
        widget.setLayout(layout)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(widget)
        

    def openAttendList(self, button):
        dialog = AttendListMenu()
        self.dialogs.append(dialog)
        dialog.show()