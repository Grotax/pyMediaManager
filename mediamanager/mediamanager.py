#!/usr/bin/python3
""" mediamanger """
import os
import medium
import database

class MediaManager():
    """ thats a MediaManager """
    def __init__(self):
        super().__init__()
        self.collection_db = None

    def create_collection(self, directory):
        """ create a new collection """
        mediamanger_path = os.path.join(directory, ".mediamanger")
        try:
            os.mkdir(mediamanger_path)
            os.mkdir(os.path.join(mediamanger_path, "thumbnails"))
        except FileExistsError:
            pass

        self.collection_db = database.Database(os.path.join(mediamanger_path, "mediamanger.db"))
        collection = []

        for file in os.listdir(directory):
            file_name = os.path.join(directory, file)
            try:
                collection.append(medium.Medium(None, file_name, []))
            except IsADirectoryError:
                pass
        for element in collection:
            self.collection_db.put(element)


def main():
    my_manager = MediaManager()
    my_manager.create_collection("some media dir")

if __name__ == '__main__':
    main()
