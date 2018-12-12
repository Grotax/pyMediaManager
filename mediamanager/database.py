""" Database adapter """
import sqlite3

class Database():
    """ interacts with the database """
    def __init__(self, database_path):
        super().__init__()
        self.database = sqlite3.connect(database_path)
        self.database_cursor = self.database.cursor()
        self.database_cursor.execute(
            """CREATE TABLE IF NOT EXISTS collection
               (medium_id text, filename text, tags text, PRIMARY KEY (medium_id, filename))""")

    def get_ids(self):
        """ returns all ids """
        return self.database_cursor.execute(
            "SELECT medium_id FROM collection").fetchall()

    def get_all(self):
        """ read all available data from database """
        return self.database_cursor.execute(
            "SELECT * FROM collection").fetchall()

    def get(self, medium_id):
        """ read data from database """
        return self.database_cursor.execute(
            "SELECT * FROM collection WHERE medium_id=?", (medium_id,)).fetchone()

    def update(self, existing_medium):
        """ update a entry in the db """
        self.database_cursor.execute(
            "UPDATE collection SET filename = ?, tags = ? WHERE medium_id = ?",
            (existing_medium.filename,
             existing_medium.get_tags(),
             existing_medium.medium_id))
        self.database.commit()

    def put(self, new_media):
        """ write data to database.
        Accepts medium object and iterable of medium objects. """
        def put_one(new_medium):
            """Inserts a single row without committing"""
            self.database_cursor.execute(
                "INSERT OR IGNORE INTO collection VALUES (?, ?, ?)",
                (new_medium.medium_id,
                 new_medium.filename,
                 new_medium.get_tags()))
        try:
            for new_medium in new_media:
                put_one(new_medium)
        except TypeError:
            put_one(new_media)
        self.database.commit()

    def delete(self, medium_id):
        """ delete a entry """
        self.database_cursor.execute(
            "DELETE FROM collection WHERE medium_id=?", (medium_id,))
        self.database.commit()
