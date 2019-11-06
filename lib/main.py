# import test
from home import Home
from PySide2.QtWidgets import *


def main():
    # test()
    app = QApplication()
    home = Home()
    home.show()
    app.exec_()

if __name__ == "__main__":
    main()