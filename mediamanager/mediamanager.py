#!/usr/bin/python3
""" mediamanger """
import os
import medium
import database

class MediaManager():
    """ thats a MediaManager """

    def create_collection(self, directory):
        """ create a new collection """
        # Create sub dir
            # Create thumbnail folder
            # Create Database
        # Read all files
            # Add files to database
        pass

    def test(self):
    # dev
        path = "some path"
        collection = []
        for file in os.listdir(path):
            file_name = os.path.join(path, file)
            collection.append(medium.Medium(None, file_name, []))
        for element in collection:
            print(element)
        print("----------------")
        for element in collection:
           print(element.mime_type(), element.medium_id)


if __name__ == '__main__':
    media_manager = MediaManager()
    media_manager.test()
