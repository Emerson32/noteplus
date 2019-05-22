import click
import datetime
import os
import shutil
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from noteplus.setup_db import init_db
from noteplus.commands.basis import Note


def add_folder(path):
    abs_path = os.path.join(os.getcwd(), path)

    if os.path.exists(abs_path):
        raise click.UsageError('Folder already exists')

    try:
        os.mkdir(abs_path)

    except FileNotFoundError:
        click.UsageError('No such file or directory')

    return abs_path


def remove_folder(path):
    if len(os.listdir()) == 0:
        os.rmdir(path)
    else:
        shutil.rmtree(path)


def navigate(path):
    os.chdir(path)


def add_note(editor, title, text, path):
    """
    Add a note to the database

    :param editor: Visual editor flag
    :param path: Destination of new note
    :param title: Title of the note to be added
    :param text: Text of the note to be added
    """
    note_title = __get_title(title)
    note_text = __get_text(editor, text)

    # Change to desired directory
    os.chdir(path)
    note_loc = os.getcwd()

    # Ensures data table is defined before insertion
    init_db()

    # Open connection to the notes database
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    time = datetime.datetime.now()
    time_stamp = time.strftime('%m-%d-%y %X')

    new_note = Note(note_title, note_text, note_loc, time_stamp)

    with conn:
        c.execute("INSERT INTO notes VALUES(:title, :note, :time_stamp)",
                  {'title': new_note.title, 'note': new_note.note,
                   'time_stamp': new_note.time_stamp})

    return new_note


def __get_title(title):
    """
    Prompts the user for the title
    :rtype: str
    :param title: The title parameter
    :return: The title
    """

    title_list = WordCompleter(['Todo', 'Untitled'])

    if not title:
        header = prompt('Title: ', completer=title_list)

        if not header:
            title = 'Untitled'

        else:
            title = header.rstrip()

    return title


def __get_text(ed, txt):
    """
    Prompts the user for the note text
    :rtype: str
    :param ed: visual editor flag
    :param txt: note text
    :return: potentially modified note text
    """

    # Visual editor option selected and text provided via command line
    if ed:
        note = click.edit()

        if note is None:
            note = ''

    elif txt:
        note = txt

    else:
        note = prompt('Note: ')

    if '' == note:
        note = 'Empty Note'

    note = note.rstrip()
    return note


def remove_note(purge, title):
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


def edit_note():
    """
    Allows the user to edit a note in the current folder.
    :return:
    """