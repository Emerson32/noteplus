import click
import datetime
import os
import shutil
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from noteplus.setup_db import init_db
from noteplus.commands.basis import Note


def add_folder(folder_name, path):
    if path != os.getcwd:
        path = os.path.join(path, folder_name)

    if os.path.exists(path):
        raise click.UsageError('Folder already exists')

    try:
        os.makedirs(path)

    except FileNotFoundError:
        click.UsageError('No such file or directory')


def remove_folder(path):
    abs_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(abs_path):
        raise click.UsageError('No such file or directory')

    # Current folder is empty
    if len(os.listdir(abs_path)) == 0:
        os.rmdir(abs_path)

    else:
        shutil.rmtree(abs_path)

    return abs_path


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


def clean_notes():
    if not os.path.isfile('notes.db'):
        raise click.UsageError('Notes file non-existent')

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    with conn:
        c.execute('SELECT * from notes')
        removed = c.fetchall()
        c.execute('DELETE from notes')

    return removed


def purge_notes():
    if not os.path.isfile('notes.db'):
        raise click.UsageError('Notes file non-existent')

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    c.execute('SELECT * from notes')
    removed = c.fetchall()

    click.secho("Removed: ", bold=True, fg='magenta', nl=False)
    click.secho((os.path.join(os.getcwd(), 'notes.db')), underline=True)
    os.remove('notes.db')

    return removed


def remove_note(title):
    """
    Remove a note

    :rtype: str
    :param purge: Remove all entries in the database
    :param title: Title of the note to be removed
    :return: Note entry removed. None is returned if note is not found
    """
    if not os.path.isfile('notes.db'):
        raise click.UsageError('Notes file non-existent. \
                                \n       See noteplus add.\v')

    conn = sqlite3.connect('notes.db')
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


def edit_note():
    """
    Allows the user to edit a note in the current folder.
    """
