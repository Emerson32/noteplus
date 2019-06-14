# remove.py - Remove a note from the notebook

import click
import os

from noteplus.commands.basis import NoteBook
from noteplus.commands.basis import Subject


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('remove', context_settings=CONTEXT_SETTINGS,
               short_help='remove a note')
@click.option('-c', '--clean', 'clean', is_flag=True,
              help='remove all notes (preserves database file)')
@click.option('--purge', 'purge', is_flag=True,
              help='remove all notebooks (removes database file)')
@click.option('-s', '--subject', 'subject',
              nargs=1, type=click.Path(writable=True),
              help='remove a folder')
@click.option('-n', '--note', 'note', nargs=1,
              help='remove a note')
@click.option('-nb', '--notebook', 'notebook',
              nargs=1, type=str, default='notes.nbdb',
              help='Specify the name of the notebook file')
@click.option('--path', 'path', nargs=1,
              type=click.Path(writable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='specific folder path of note')
def remove(clean, purge, subject, note, notebook, path):
    """Remove a note from the database"""

    if os.path.exists(path):
        os.chdir(path)
    else:
        raise click.UsageError("No such file or directory")

    if subject:
        subject_name = os.path.basename(subject.rstrip('/'))
        abs_path = os.path.join(os.getcwd(), subject)
        subj = Subject(path=abs_path, name=subject_name)
        removed_subject = subj.remove()
        click.echo("Removed: " + removed_subject)

    elif note:
        # Invalid file for removal operation
        if '.nbdb' not in notebook:
            raise click.UsageError("NoteBook named \'" + notebook + "\' cannot be removed")

        note_book = NoteBook(path=path, file_name=notebook)
        note_book.remove_note(note)

    elif clean:
        if '.nbdb' not in notebook:
            raise click.UsageError("NoteBook named \'" + notebook + "\' cannot be removed")

        note_book = NoteBook(path=path, file_name=notebook)
        if click.confirm('\nRemove all notes in the provided notebook?'):
            note_book.clean_notes()

    # Only removes .nbdb files
    elif purge:
        if click.confirm('\nRemove all notebooks in the current subject?'):

            for file in os.listdir(path):
                if file.endswith('.nbdb'):
                    note_book = NoteBook(path=path, file_name=file)
                    note_book.remove()

    elif notebook:
        if '.nbdb' not in notebook:
            raise click.UsageError("NoteBook named \'" + notebook + "\' cannot be removed")

        note_book = NoteBook(path=path, file_name=notebook)
        note_book.remove()

    else:
        raise click.BadOptionUsage('Missing option')