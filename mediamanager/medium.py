""" defines a medium """

import magic

class Medium():
    """ a Medium """
    def __init__(self, filename):
        super(Medium, self).__init__()
        self.filename = filename

    def media_type(self):
        return magic.from_file(self.filename, mime=True)

    def rename(self):


    def tags(self):