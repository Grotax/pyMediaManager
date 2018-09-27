#!/usr/bin/python3
""" The gui for mediamanager """
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QGridLayout, QBoxLayout, QWidget

class DetailView(QBoxLayout):
    """docstring for DetailView"""
    def __init__(self):
        super().__init__()

class OverView(QGridLayout):
    """docstring for OverView"""
    def __init__(self):
        super().__init__()


class Search(QBoxLayout):
    """docstring for Search"""
    def __init__(self):
        super().__init__(QBoxLayout.LeftToRight)
        self.searchbar = QLineEdit()
        self.addWidget(self.searchbar)


class MainWindow(QMainWindow):
    """docstring for MainWindow"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('The Python Media Manager')
        self.main_widget = QWidget()
        self.main_grid = QGridLayout()

        self.searchbar = QLineEdit()
        self.main_grid.addWidget(self.searchbar, 1, 0)

        self.main_widget.setLayout(self.main_grid)

        self.setCentralWidget(self.main_widget)

        #self.over_view = OverView()
        #self.search = Search()
        #self.main_grid.addItem(self.search, 0, 0)

        #self.main_grid.addItem(self.over_view, 0, 1)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2 / 3)
    mainWin.show()
    sys.exit(app.exec_())