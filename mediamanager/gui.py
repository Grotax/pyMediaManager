#!/usr/bin/python3
""" The gui for mediamanager """
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit


class MainWindow(QMainWindow):
    """docstring for MainWindow"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('The Python Media Manager')
        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)
        self.addToolBar(self.toolBar)
        self.addressLineEdit = QLineEdit()
        self.toolBar.addWidget(self.addressLineEdit)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2 / 3)
    mainWin.show()
    sys.exit(app.exec_())