# basis.py
# Object representing each note entered by the user


class Note:
    """Note class"""
    def __init__(self, title, note, path, time_stamp):
        self.title = title
        self.note = note
        self.path = path
        self.time_stamp = time_stamp

    def to_string(self):
        return 'Location: ' + self.path + '\nTitle: ' + self.title + '\nNote: ' + self.note +\
               '\nTime Stamp: ' + self.time_stamp + '\n'


class Folder:
    """Folder class"""
    def __init__(self, name, path, date_created):
        self.name = name
        self.path = path
        self.date_created = date_created
