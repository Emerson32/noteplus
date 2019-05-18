# basis.py
# Object representing each note entered by the user


class Note:

    def __init__(self, title, note, time_stamp):
        self.title = title
        self.note = note
        self.time_stamp = time_stamp
