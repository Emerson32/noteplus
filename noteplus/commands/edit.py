# edit.py - Edit the contents of a note entry
import click
import os

from noteplus.commands.basis import NoteBook

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('edit', context_settings=CONTEXT_SETTINGS,
               short_help='edit a note')
@click.option('-n', '--note', 'note',
              nargs=1, type=str,
              help='edit the text of a given note entry (arg = title)')
@click.option('-nb', '--notebook', 'notebook', nargs=1,
              type=str, default='notes.nbdb',
              show_default=True,
              help='Name of notes file to edit')
@click.option('-p', '--path', 'path', nargs=1,
              type=click.Path(writable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='Specific path for desired notes file')
def edit(note, path, notebook):
    """Make changes to a note or folder"""
    if os.path.exists(path):
        os.chdir(path)
    else:
        raise click.UsageError("No such file or directory")

    if note:
        if not os.path.isfile(notebook):
            raise click.UsageError('Notes file named: '
                                   + notebook + ' does not exist'
                                   + ' within the provided path')

        note_book = NoteBook(path=path, file_name=notebook)
        note_book.edit(note_title=note)

    else:
        raise click.UsageError('Missing option')
