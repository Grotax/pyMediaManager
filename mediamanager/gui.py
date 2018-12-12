#!/usr/bin/python3
""" The gui for mediamanager """
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QGridLayout, QBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QScrollArea
from PySide2.QtGui import QMovie
from . import manager

class DetailView(QBoxLayout):
    """docstring for DetailView"""
    def __init__(self):
        super().__init__()

class Medium(QVBoxLayout):
    """ """
    def __init__(self, medium):
        super().__init__()
        self.addWidget(QLabel("Bild"))
        self.addWidget(QLabel(medium.filename))
        self.addWidget(QLabel("".join(medium.tags)))

class OverView(QGridLayout):
    """docstring for OverView"""
    def __init__(self):
        super().__init__()
        #self.update()
    def update(self, media):
        x = 0
        y = 0
        for medium in media:
            if y > 1:
                x += 1
                y = 0
            self.addLayout(Medium(medium), x, y)
            y += 1


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

        self.over_view_widget = QWidget()
        self.over_view = OverView()
        self.over_view_widget.setLayout(self.over_view)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.over_view_widget)
        self.scroll_area.setWidgetResizable(True)

        self.search = Search()
        self.main_grid.addLayout(self.search, 0, 0)
        self.main_grid.addWidget(self.scroll_area, 1, 0)

        self.button_loading = QBoxLayout(QBoxLayout.LeftToRight)
        self.button = QPushButton("Open Collection")
        self.button.clicked.connect(self.open_folder)

        self.loader_widget = QLabel("Loading...")
        #self.loader_animation = QMovie("assets/loader.gif")
        #self.loader_widget.setMovie(self.loader_animation)
        self.loader_widget.setVisible(False)

        self.button_loading.addWidget(self.button)
        self.button_loading.addWidget(self.loader_widget)

        self.main_grid.addLayout(self.button_loading, 2, 0, 1)

        self.main_grid.addWidget(self.loader_widget, 2, 1, 1)
        self.main_widget.setLayout(self.main_grid)
        self.setCentralWidget(self.main_widget)

        self.media_manager = manager.MediaManager()
        self.media_manager.register_observer(self)

    def open_folder(self):
        dialog = QFileDialog(self)
        directory = dialog.getExistingDirectory(self)
        self.button.setEnabled(False)
        self.loader_widget.setVisible(True)
        self.media_manager.create_collection(directory)

    def recieve(self):
        self.over_view.update(self.media_manager.get_all_media())
        self.button.setEnabled(True)
        self.loader_widget.setVisible(False)

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    available_geometry = app.desktop().availableGeometry(main_window)
    main_window.resize(available_geometry.width() * 2 / 3, available_geometry.height() * 2 / 3)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
