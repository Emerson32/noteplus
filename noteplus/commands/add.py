# add.py - Create a new entry through the usage of your default editor
#           or through the command line
import click
import datetime
import sqlite3

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from noteplus.commands.basis import Note

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('add', context_settings=CONTEXT_SETTINGS, short_help='add note entries')
@click.option('-e', '--editor', 'editor', is_flag=True, help='use buffer to enter note')
@click.argument('title', required=False, type=str)
@click.argument('text', required=False, type=str)
def add(editor, text, title):
    """Add a new note to the notebook"""
    note_title = get_title(title)
    note_text = get_text(editor, text)

    add_to_notebook(note_title, note_text)

    print(note_title)
    print(note_text)


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


def get_text(ed, txt):
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


def add_to_notebook(header, txt):
    """
    Adds a note to the notebook
    :param header: header/title of the note
    :param txt: text of the note
    """

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    time = datetime.datetime.now()
    time_stamp = time.strftime("%m-%d-%y %X")
    click.echo(time_stamp)

    new_note = Note(header, txt, time_stamp)

    c.execute("INSERT INTO notes VALUES(:title, :note, :time_stamp)",
              {'title': new_note.title, 'note': new_note.note,
                  'time_stamp': new_note.time_stamp})

    conn.commit()
    conn.close()
