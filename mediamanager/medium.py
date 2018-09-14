""" defines a medium """

import os
import json
import hashlib
import magic

class Medium():
    """ a Medium """
    medium_id = ""
    filename = ""
    tags = []

    def __init__(self, medium_id, filename, tags):
        super().__init__()
        self.filename = filename
        if medium_id is None:
            self.create_media_id()
        else:
            self.medium_id = medium_id
        self.load_tags(tags)

    def __str__(self):
        return self.filename

    def __repr__(self):
        string = """medium.Medium('{}', '{}', '{}')""".format(
            self.medium_id, self.filename, json.dumps(self.tags))
        return string

    def __eq__(self, other):
        vals = []
        vals.append(self.medium_id == other.medium_id)
        vals.append(self.tags == other.tags)
        vals.append(self.filename == other.filename)

        return all(vals)

    def mime_type(self):
        """ returns mime type """
        return magic.from_file(self.filename, mime=True)

    def rename(self, name):
        """ renames the file """
        os.rename(self.filename, name)
        self.filename = name

    def load_tags(self, tag_string):
        """ parse tags from string """
        try:
            self.tags = json.loads(tag_string)
        except TypeError:
            self.tags = []

    def add_tags(self, tag_string):
        """ add one ore more tags """
        self.tags.append(tag_string)

    def get_tags(self):
        """ returns all tags as json """
        return json.dumps(self.tags)

    def delete_tag(self, tag_string):
        """ delete a tag """
        self.tags.remove(tag_string)

    def contains(self, tag_string):
        """ returns true when tag exists """
        return tag_string in self.tags

    def create_media_id(self):
        """ creates new hash """
        buffer_size = 65536
        sha2 = hashlib.sha256()

        with open(self.filename, 'rb', buffering=0) as file:
            while True:
                data = file.read(buffer_size)
                if not data:
                    break
                sha2.update(data)
        self.medium_id = sha2.hexdigest()
