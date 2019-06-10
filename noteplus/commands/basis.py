# basis.py
# Object representing each note entered by the user
import click
import datetime
import os
import shutil
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


class NoteBook:
    """Class representing note database"""
    def __init__(self, path, file_name):
        self.path = os.path.abspath(path)
        self.dbfilename = file_name

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS notes (
                            title text,
                            note_entry text,
                            time_stamp text
                            )""")
            conn.commit()

    def add(self, note):
        # Open connection to the notes database
        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute("INSERT INTO notes VALUES(:title, :note_entry, :time_stamp)",
                      {'title': note.get_title(), 'note_entry': note.get_text(),
                       'time_stamp': note.get_timestamp()})

    def clean_notes(self):

        if not os.path.isfile(self.dbfilename):
            raise click.UsageError('Notes file non-existent')

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * from notes')
            removed = c.fetchall()
            c.execute('DELETE from notes')

        return removed

    def purge_notes(self):
        if not os.path.isfile(self.dbfilename):
            raise click.UsageError('Notes file non-existent')

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        c.execute('SELECT * from notes')
        removed = c.fetchall()

        click.secho("Removed: ", bold=True, fg='magenta', nl=False)
        click.secho((os.path.join(os.getcwd(), self.dbfilename)), underline=True)
        os.remove(self.dbfilename)

        return removed

    def remove_note(self, title):
        """
        Remove a note

        :rtype: str
        :param title: Title of the note to be removed
        :return: Note entry removed. None is returned if note is not found
        """
        if not os.path.isfile(self.dbfilename):
            raise click.UsageError('Notes file non-existent. \
                                    \n       See noteplus add.\v')

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * from notes WHERE title=:title',
                      {'title': title})
            removed = c.fetchall()

            if len(removed) == 0:
                raise click.UsageError('No such note with that title')
            elif len(removed) > 1:
                # Present user with menu to choose a note
                pass
            else:
                c.execute('DELETE from notes WHERE title=:title',
                          {'title': title})

        return removed

    def retrieve_all(self):

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * FROM notes')

        results = c.fetchall()
        return results

    def retrieve_by_title(self, title):
        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * FROM notes WHERE title=:title',
                      {'title': title})

        results = c.fetchall()
        return results

    def retrieve_by_note(self, note):
        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('Select * FROM notes WHERE note=:note',
                      {'note': note})

        results = c.fetchall()
        return results

    def rename(self, old_title, new_title):
        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * FROM notes WHERE title=:title',
                      {'title': old_title})

            results = c.fetchall()

        if len(results) == 0:
            raise click.UsageError('No such note with that title')
        elif len(results) > 1:
            # Present user with menu to choose a note
            pass
        else:
            # Update one entry with the new title
            with conn:
                c.execute('''UPDATE notes set title= ?
                          WHERE title= ? ''',
                          (new_title, old_title))

    def edit(self, note_title):

        conn = sqlite3.connect(self.dbfilename)
        c = conn.cursor()

        with conn:
            c.execute('SELECT * from notes WHERE title=:title',
                      {'title': note_title})

        results = c.fetchall()

        if len(results) == 0:
            raise click.UsageError('No such note with that title')
        elif len(results) > 1:
            # Present user with menu to choose a note
            pass
        else:
            target_note = results[0]
            new_txt = click.edit(target_note[1])

            if not new_txt:
                new_txt = note_title

            with conn:
                c.execute('''UPDATE notes set note=?
                           WHERE title=?''',
                          (new_txt, note_title))

    def to_string(self):
        return 'Location: ' + self.path + '\nFile Name: ' + self.dbfilename


class Note:
    """Class representing note entry"""
    def __init__(self, title, text, path):
        time = datetime.datetime.now()
        stamp = time.strftime('%m-%d-%y %X')

        self.title = title
        self.text = text
        self.path = os.path.abspath(path)
        self.time_stamp = stamp

    def get_title(self):
        return str(self.title)

    def get_text(self):
        return str(self.text)

    def get_timestamp(self):
        return str(self.time_stamp)

    def set_title(self, title):
        """
            Prompts the user for the title
            :param note: Note object
            :param title: The title parameter
            """

        title_list = WordCompleter(['Todo', 'Untitled'])

        if not title:
            header = prompt('Title: ', completer=title_list)

            if not header:
                self.title = 'Untitled'

            else:
                self.title = header.rstrip()
        else:
            self.title = title

    def set_text(self, editor, text):
        """
            Prompts the user for the note text
            :param editor: visual editor flag
            :param text: note text
            """

        # Visual editor option selected and text provided via command line
        if editor:
            self.text = click.edit()

            if self.text is None:
                self.text = ''

        elif text:
            self.text = text

        else:
            self.text = prompt('Note: ')

        if '' == self.text:
            self.text = 'Empty Note'

    def to_string(self):
        return '\nLocation: ' + self.path + '\n\nTitle: ' + self.title \
                + '\nNote: ' + self.text + '\nDate: ' + self.time_stamp


class Subject:
    """Folder class"""
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def create(self):
        if self.path != os.getcwd:
            self.path = os.path.join(self.path, self.name)

        if os.path.exists(self.path):
            raise click.UsageError('Folder already exists')

        try:
            os.makedirs(self.path)

        except FileNotFoundError:
            click.UsageError('No such file or directory')

    def remove(self):
        abs_path = os.path.join(os.getcwd(), self.path)

        if not os.path.exists(abs_path):
            raise click.UsageError('No such file or directory')

        # Current folder is empty
        if len(os.listdir(abs_path)) == 0:
            os.rmdir(abs_path)

        else:
            shutil.rmtree(abs_path)

        return abs_path
