""" Database adapter """
import sqlite3
import medium

class Database():
    """ interacts with the database """
    def __init__(self, config):
        super().__init__()
        self.database = sqlite3.connect(config["databasepath"])
        self.database_cursor = self.database.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS history (medium_id text, file_name text, tags text)")

    def get_ids(self):
        """ returns all ids """
        return self.database_cursor.execute("SELECT medium_id FROM collection").fetchall()

    def get_all(self):
        """ read all available data from database """
        self.database_cursor.execute("SELECT * FROM collection").fetchall()

    def get(self, existing_medium):
        """ read data from database """
        self.database_cursor.execute("SELECT * FROM collection WHERE medium_id=?", (existing_medium.medium_id,))

    def update(self, existing_medium):
        """ update a entry in the db """
        self.database_cursor.execute("UPDATE collection SET file_name = ?, tags = ?",
                                     (existing_medium.file_name, existing_medium.tags))

    def put(self, new_medium):
        """ write data to database """
        self.database_cursor.execute("INSERT INTO collection VALUES (?, ?, ?)",
                                     (new_medium.medium_id, new_medium.file_name, new_medium.tags))
        self.database.commit()

    def delete(self, medium_id):
        """ delete a entry """
        self.database_cursor.execute("DELETE FROM collection WHERE medium_id=?", (medium_id,))
        self.database.commit()
