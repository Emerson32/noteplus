import click
import datetime
import os
import shutil
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

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
    :param title: Title of the note to be added
    :param text: Text of the note to be added
    :param path: Destination of new note
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


def get_title(title):
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


def get_text(editor, text):
    """
    Prompts the user for the note text
    :rtype: str
    :param editor: visual editor flag
    :param text: note text
    :return: potentially modified note text
    """

    # Visual editor option selected and text provided via command line
    if editor:
        note = click.edit()

        if note is None:
            note = ''

    elif text:
        note = text

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


def rename_title(old_title, new_title):
    """
    Allows the user to edit a note in the current folder.
    """
    conn = sqlite3.connect('notes.db')
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


def edit_note(note_title):
    if not os.path.isfile('notes.db'):
        raise click.UsageError('Notes file non-existent. \
                                \n       See noteplus add.\v')

    conn = sqlite3.connect('notes.db')
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





