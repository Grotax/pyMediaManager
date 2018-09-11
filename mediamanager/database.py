""" Database adapter """
import sqlite3
import sys
import hashlib
from . import medium

class Database():
    """ interacts with the database """
    def __init__(self, config):
        super(Database, self).__init__()
        self.database = sqlite3.connect(config["databasepath"])
        self.database_cursor = self.database.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS history (medium_id text, file_name text, tags text)")

    def get_ids(self):
        """ returns all ids """
        return self.database_cursor.execute("SELECT medium_id FROM collection").fetchall()

    def get_all(self):
        """ read all available data from database """
        self.database_cursor.execute("SELECT * FROM collection").fetchall()

    def get(self, medium_id):
        """ read data from database """
        self.database_cursor.execute("SELECT * FROM collection WHERE medium_id=?", (medium_id,))

    def update(self):
        ""
    def put(self, medium):
        """ write data to database """
        buffer_size = 65536
        sha2 = hashlib.sha256()

        with open(medium.filename, 'rb', buffering=0) as file:
            while True:
                data = file.read(buffer_size)
                if not data:
                    break
                sha2.update(data)

        medium_id = sha2.hexdigest()
        self.database_cursor.execute("INSERT INTO collection WHERE (medium_id, file_name, tags)", (medium_id,))
        self.database.commit()

    def delete(self, medium_id):
        """ delete a entry """
        self.database_cursor.execute("DELETE FROM collection WHERE medium_id=?", (medium_id,))
        self.database.commit()






