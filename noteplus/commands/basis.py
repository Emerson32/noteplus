# basis.py
# Object representing each note entered by the user


class Note:
    """Note class"""
    def __init__(self, title, note, time_stamp):
        self.title = title
        self.note = note
        self.time_stamp = time_stamp


class Folder:
    """Folder class"""
    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created
