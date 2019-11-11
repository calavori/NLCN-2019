import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from data import Data
from tableModel import MyTableModel

class AttendListMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Attendance List')
        self.layout = QVBoxLayout()
        self.label = QLabel('Danh sách điểm danh')
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)

        # 
        self.date = QDateEdit()
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date.setMaximumDate(QDate(7999, 12, 28))
        self.date.setCalendarPopup(True)
        
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(lambda: self.showAttend(self.okButton, self.date.date()))
        
        
        self.table_view = QTableView()
        

        # 
        self.widgets = [self.label, self.date, self.okButton, self.table_view]
        for w in self.widgets:
            self.layout.addWidget(w)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.widget)    

    def qdateToStr(self, qdate):
        qdate = str(qdate).split('(')
        temp = qdate[1]
        temp = temp[:-1]
        temp = temp.split(',')
        date = temp[0].strip() + '-' + temp[1].strip() + '-' + temp[2].strip()
        return date

    def showAttend(self, button, qdate):
        date = self.qdateToStr(qdate)
        data = Data()
        list = data.getDb_attendace(date)
        print(list)
        header = ['Student ID', 'Student Name', 'Data ID', 'Time', 'Status']

        self.table_view.clearSpans()
        table_model = MyTableModel(self, list, header)
        self.table_view.setModel(table_model)
        self.table_view.resizeColumnsToContents()
        self.resize(500, 500)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        



             