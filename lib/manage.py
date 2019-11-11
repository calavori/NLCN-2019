import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from data import Data
from label_training import Label_training
from tableModel import MyTableModel

class ManageMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = Data()

        self.setWindowTitle('Data Manage')
        self.layout = QVBoxLayout()
        self.label = QLabel('Quản lý dữ liệu')
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)

        self.idBox = QLineEdit()
        self.id = ''
        self.idBox.setPlaceholderText('Nhập ID')
        self.idBox.textChanged.connect(self.id_changed)

        self.nameBox = QLineEdit()
        self.name =''
        self.nameBox.setPlaceholderText('Nhập Tên')
        self.nameBox.textChanged.connect(self.name_changed)

        self.addDataButton = QPushButton('Thêm dữ liệu khuôn mặt')
        self.addDataButton.clicked.connect(lambda: self.addData(self.addDataButton))

        self.searchBox = QLineEdit()
        self.search = ''
        self.searchBox.setPlaceholderText('Nhập từ khóa')
        self.searchBox.textChanged.connect(self.search_changed)

        self.searchButton = QPushButton('Tìm kiếm')
        self.searchButton.clicked.connect(lambda: self.searchData(self.searchButton))

        self.updateButtton = QPushButton('Cập nhật dữ liệu khuôn mặt')
        self.updateButtton.clicked.connect(lambda: self.updateData())

        self.editDbButton = QPushButton('Lưu thay đổi thông tin')
        self.editDbButton.clicked.connect(lambda: self.editDb())

        self.id2Box = QLineEdit()
        self.id2 = ''
        self.id2Box.setPlaceholderText('Nhập ID')
        self.id2Box.textChanged.connect(self.id2_changed)

        self.editFaceButtton = QPushButton('Thay đổi dữ liệu khuôn mặt')
        self.editFaceButtton.clicked.connect(lambda: self.editFaceData())

        self.delDataButtton = QPushButton('Xóa dữ liệu')
        self.delDataButtton.clicked.connect(lambda: self.delData())

        # Tao bang
        self.table_view = QTableView()
        header = ['ID', 'Name']
        dataList =[]
        raw_data = self.data.getDb_students()
        for x in raw_data:
            y = [x[0], x[1]]
            dataList.append(y)
        self.tableModel = MyTableModel(self, dataList, header)
        self.table_view.setModel(self.tableModel)
        
        

        self.widgets = [self.label, self.idBox, self.nameBox, self.addDataButton, self.searchBox, self.searchButton, self.table_view, self.editDbButton, self.id2Box, self.editFaceButtton, self.delDataButtton, self.updateButtton]
        for w in self.widgets:
            self.layout.addWidget(w)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.widget) 

    def id_changed(self, text):
        self.id = text

    def name_changed(self, text):
        self.name = text

    def search_changed(self, text):
        self.search = text

    def id2_changed(self, text):
        self.id2 = text

    def addData(self, button):
        # print(self.id)
        # print(self.name)
        self.data.addDb_student(self.id, self.name)
        self.data.add_data(self.id)
        self.noti('Đã thêm dữ liệu thành công')
        self.updateTable()

    def searchData(self, button):
        dataList =[]
        raw_data = self.data.SearchDb_students(self.search)
        for x in raw_data:
            y = [x[0], x[1]]
            dataList.append(y)
        self.table_view.clearSpans
        header = ['ID', 'Name']
        tableModel = MyTableModel(self, dataList, header)
        self.table_view.setModel(tableModel)

    def updateData(self):
        Label_training.train()

    def editDb(self):
        model = self.tableModel
        data = []
        for row in range(model.rowCount(ManageMenu)):
            data.append([])
            for column in range(model.columnCount(ManageMenu)):
                index = model.index(row, column)
                data[row].append(str(model.data(index, Qt.DisplayRole)))
        for i in data:
            self.data.editDb_studentName(i[0], i[1])

    def editFaceData(self):
        id = self.id2
        self.data.edit_data(id)
        self.noti('Đã chỉnh sửa dữ liệu thành công')
        self.updateTable()
        

    def delData(self):
        id = self.id2
        self.data.del_data(id)
        self.noti('Đã xóa dữ liệu thành công')
        self.updateTable()

    def updateTable(self):
        header = ['ID', 'Name']
        dataList =[]
        raw_data = self.data.getDb_students()
        for x in raw_data:
            y = [x[0], x[1]]
            dataList.append(y)
        self.tableModel = MyTableModel(self, dataList, header)
        self.table_view.setModel(self.tableModel)

    def noti(self, str):
        dialog = QMessageBox()
        dialog.setWindowTitle('Thông báo')
        dialog.setText(str)
        dialog.setStandardButtons(QMessageBox.Yes)
        yes = dialog.button(QMessageBox.Yes)
        yes.setText('OK')
        dialog.exec_()