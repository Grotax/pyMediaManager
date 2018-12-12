#!/usr/bin/python3
""" mediamanger """
import os

from PySide2.QtCore import QRunnable, QThreadPool, QObject, Signal

from . import medium
from . import database

class ScannerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    '''
    result = Signal(list)

class Scanner(QRunnable):
    """ Scan a directory """
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.signals = ScannerSignals()

    def run(self):
        collection = []

        for file in os.listdir(self.directory):
            file_name = os.path.join(self.directory, file)
            try:
                collection.append(medium.Medium(None, file_name, []))
            except IsADirectoryError:
                pass
        self.signals.result.emit(collection)

class MediaManager(QObject):
    """ thats a MediaManager """
    def __init__(self):
        super().__init__()
        self.collection_db = None
        self.observers = []
        self.threadpool = None

    def register_observer(self, observer):
        """ register a new observer """
        self.observers.append(observer)

    def notify_observers(self):
        """ notify all the observers """
        for observer in self.observers:
            observer.recieve()

    def create_collection(self, directory):
        """ create a new collection """
        if directory == "":
            return
        mediamanger_path = os.path.join(directory, ".mediamanger")
        try:
            os.mkdir(mediamanger_path)
            os.mkdir(os.path.join(mediamanger_path, "thumbnails"))
        except FileExistsError:
            pass

        self.collection_db = database.Database(os.path.join(mediamanger_path, "mediamanger.db"))

        self.threadpool = QThreadPool()
        scanner = Scanner(directory)
        scanner.signals.result.connect(self.write_to_db)
        self.threadpool.start(scanner)

    def write_to_db(self, var):
        self.collection_db.put(var)
        self.notify_observers()

    def update_collection(self):
        """ rescan direcotry and add new files """
        # TODO
        pass

    def delete_medium(self, delete_file=False):
        """ delete medium from db, delete thumbnail
            optional: delete file on disk           """
        # TODO
        pass

    def update_medium(self):
        """ edit a medium """
        # TODO
        pass

    def get_medium(self, medium_id):
        """ returns medium with id """
        medium_data = self.collection_db.get(medium_id)
        return medium.Medium(medium_data.medium_id, medium_data.filename, medium_data.tags)


    def get_medium_ids(self):
        """ returns all ids """
        return self.collection_db.get_ids()

    def get_all_media(self):
        """ returns all medium files """
        media = []
        medium_data_all = self.collection_db.get_all()
        for medium_data in medium_data_all:
            media.append(medium.Medium(medium_data[0], medium_data[1], medium_data[2]))
        return media

    def search(self, pattern):
        """ search in collection """
        # TODO
        pass