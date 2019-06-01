import click
import os
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


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






