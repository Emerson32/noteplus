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
@click.option('-p', '--purge', 'purge', is_flag=True,
              help='remove all notes (removes database file)')
@click.option('-s', '--subject', 'subject',
              nargs=1, type=click.Path(writable=True),
              help='remove a folder')
@click.option('-n', '--note', 'note', nargs=1,
              help='remove a note')
@click.option('-nb', '--notebook', 'notebook',
              nargs=1, type=str, default='notes.db',
              help='Specify the name of the notebook file')
@click.option('-p', '--path', 'path', nargs=1,
              type=click.Path(writable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='specific folder path of note')
def remove(clean, purge, subject, note, notebook, path):
    """Remove a note from the database"""

    if os.path.exists(path):
        os.chdir(path)
        note_book = NoteBook(path=path, file_name=notebook)
    else:
        raise click.UsageError("No such file or directory")

    if subject:
        subject_name = os.path.basename(subject.rstrip('/'))
        abs_path = os.path.join(os.getcwd(), subject)
        subj = Subject(path=abs_path, name=subject_name)
        removed_subject = subj.remove()
        click.echo("Removed: " + removed_subject)

    elif note:
        note_book.remove_note(note)

    elif clean:
        if click.confirm('\nRemove all notes in the provided notebook?'):
            note_book.clean_notes()

    # TODO: Make the purge option remove all notebook files exclusively
    elif purge:
        if click.confirm('\nRemove all notebooks in the current subject?'):
            note_book.purge_notes()

    elif notebook:
        note_book.remove()

    else:
        raise click.BadOptionUsage('Missing option')