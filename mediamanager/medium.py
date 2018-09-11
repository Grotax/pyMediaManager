#!/usr/bin/python3
""" defines a medium """

import magic
import re
import os
import json

class Medium():
    """ a Medium """
    def __init__(self, media_id, filename, tags):
        super(Medium, self).__init__()
        self.filename = filename
        self.media_id = media_id
        self.tags = self.load_tags(tags)

    def media_type(self):
        return magic.from_file(self.filename, mime=True)

    def rename(self, name):
        os.rename(self.filename, name)
        self.filename = name

    def load_tags(self, tag_string):
        """ parse tags from string """
        try:
            return json.loads(tag_string)
        except TypeError:
            return {}

    def add_tags(self, tag_string):
        """ add one ore more tags """
        for tag in re.finditer("(\\w+)\\s*:\\s*(\\w+)", tag_string):
            self.tags[tag.group(1)] = tag.group(2)

    def delete_tag(self, tag):
        """ delete a tag """
        # TODO
        pass
