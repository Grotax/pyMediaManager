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
            media.append(medium.Medium(medium_data.medium_id, medium_data.filename, medium_data.tags))
        return media


    def search(self, pattern):
        """ search in collection """
        # TODO
        pass

def main():
    my_manager = MediaManager()
    my_manager.create_collection("some media dir")

if __name__ == '__main__':
    main()
