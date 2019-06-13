# add.py - Create a new entry through the usage of your default editor
#           or through the command line
import click
import os

from noteplus.commands.basis import NoteBook
from noteplus.commands.basis import Note
from noteplus.commands.basis import Subject


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('add', context_settings=CONTEXT_SETTINGS,
               short_help='Add notes and/or folders')
@click.option('-s', '--subject', 'subject', nargs=1,
              type=click.Path(writable=True),
              help='Create a new subject')
@click.option('-nb', '--notebook', 'notebook',
              type=str, default='notes.db',
              show_default=True,
              help='Specify the name of a notebook')
@click.option('-n', '--note', 'note', nargs=2,
              type=str, default=None,
              help='Add a new note entry [args: (title, text)]')
@click.option('-p', '--path', 'path',
              type=click.Path(writable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='Specific path to insert notes file')
def add(subject, notebook, note, path):
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

        new_note = Note(title=note[0], text=note[1], path=file_path)

        # Must change to the desired directory before initialization
        os.chdir(file_path)

        note_book = NoteBook(path=file_path, file_name=notebook)
        note_book.add(new_note)

        click.secho(new_note.to_string(), fg='green')

    elif subject:
        new_dir = Subject(path=path, name=subject)
        new_dir.create()

    elif note:

        note_book = NoteBook(path=path, file_name=notebook)

        new_note = Note(title=note[0], text=note[1], path=path)
        note_book.add(new_note)

        click.secho(new_note.to_string(), fg='green')

    elif notebook:
        note_book = NoteBook(path=path, file_name=notebook)
        click.secho(note_book.to_string(), fg='green')

    else:
        raise click.UsageError('Missing option')
