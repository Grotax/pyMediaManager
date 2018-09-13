""" Database adapter """
import sqlite3
import medium

class Database():
    """ interacts with the database """
    def __init__(self, databasepath):
        super().__init__()
        self.database = sqlite3.connect(databasepath)
        self.database_cursor = self.database.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS collection (medium_id text PRIMARY KEY, filename text, tags text)")

    def get_ids(self):
        """ returns all ids """
        return self.database_cursor.execute("SELECT medium_id FROM collection").fetchall()

    def get_all(self):
        """ read all available data from database """
        return self.database_cursor.execute("SELECT * FROM collection").fetchall()

    def get(self, medium_id):
        """ read data from database """
        return self.database_cursor.execute("SELECT * FROM collection WHERE medium_id=?", (medium_id,))

    def update(self, existing_medium):
        """ update a entry in the db """
        self.database_cursor.execute("UPDATE collection SET filename = ?, tags = ? WHERE medium_id = ?",
                                     (existing_medium.filename, existing_medium.get_tags(), existing_medium.medium_id))

    def put(self, new_medium):
        """ write data to database """
        self.database_cursor.execute("INSERT INTO collection VALUES (?, ?, ?)",
                                     (new_medium.medium_id, new_medium.filename, new_medium.get_tags()))
        self.database.commit()

    def delete(self, medium_id):
        """ delete a entry """
        self.database_cursor.execute("DELETE FROM collection WHERE medium_id=?", (medium_id,))
        self.database.commit()
