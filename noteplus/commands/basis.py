# basis.py
# Object representing each note entered by the user
import click
import sqlite3


class Note:
    """Note class"""
    def __init__(self, title, note, time_stamp):
        self.title = title
        self.note = note
        self.time_stamp = time_stamp

    def add(editor, title, text):
        """
        Add a note to the database

        :param editor: Visual editor flag
        :param title: Title of the note to be added
        :param text: Text of the note to be added
        """

    def remove(purge, title):
        """
        Remove a note

        :param purge: Remove all entries in the database
        :param title: Title of the note to be removed
        """
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()

        if purge:
            with conn:
                c.execute('DELETE from notes')

        elif title:
            with conn:
                c.execute('DELETE from notes WHERE title=:title',
                        {'title': title})

        else:
            raise click.UsageError('Missing option or argument')


class Folder:
    """Folder class"""
    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created
