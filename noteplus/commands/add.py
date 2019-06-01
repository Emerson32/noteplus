# add.py - Create a new entry through the usage of your default editor
#           or through the command line
import click
import os

from noteplus.commands.basis import NoteBook
from noteplus.commands.basis import Note
from noteplus.commands.basis import Subject

from noteplus.commands.operations import get_title, get_text

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('add', context_settings=CONTEXT_SETTINGS,
               short_help='Add notes and/or folders')
@click.option('-e', '--editor', 'editor', is_flag=True,
              help='Use buffer to enter note')
@click.option('-s', '--subject', 'subject', nargs=1,
              type=click.Path(writable=True),
              help='Create a new subject')
@click.option('-nb', '--notebook', 'notebook', nargs=1,
              type=str, default='notes.db',
              help='Specify the name of a notebook (default = notes.db)')
@click.option('-n', '--note', 'note', is_flag=True,
              help='Add a new note entry')
@click.option('-p', '--path', 'path',
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              type=click.Path(writable=True),
              help='Specified path')
@click.argument('title', required=False, default='', type=str)
@click.argument('text', required=False, default='', type=str)
def add(editor, subject, notebook, note, path, title, text):
    """Add a new note to the notebook"""
    # First handle the provided path
    if not os.path.exists(path):
        raise click.UsageError('No such file or directory')

    else:
        os.chdir(path)

    if subject and note:
        # Create the folder with the given path.
        # The path is the current directory by default.
        new_dir = Subject(path=path, name=subject)
        new_dir.create()

        # In this case an extended path must be created
        # so the file is stored within the created directory
        file_path = os.path.join(path, subject)

        # Unreachable path created
        if not os.path.exists(file_path):
            raise click.UsageError('No such file or directory')

        note_title = get_title(title=title)
        note_text = get_text(editor=editor, text=text)
        new_note = Note(title=note_title, text=note_text, path=file_path)

        # Must change to the desired directory before initialization
        os.chdir(file_path)

        note_book = NoteBook(path=file_path, file_name=notebook)
        note_book.add(new_note)

        click.secho(new_note.to_string(), fg='green')

    elif subject:
        new_dir = Subject(path=path, name=subject)
        new_dir.create()

    elif note:
        note_title = get_title(title=title)
        note_text = get_text(editor=editor, text=text)
        new_note = Note(title=note_title, text=note_text, path=path)

        note_book = NoteBook(path=path, file_name=notebook)
        note_book.add(new_note)

        click.secho(new_note.to_string(), fg='green')

    else:
        raise click.UsageError('Missing option')
