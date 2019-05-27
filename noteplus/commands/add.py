# add.py - Create a new entry through the usage of your default editor
#           or through the command line
import click
import os

from noteplus.commands.operations import add_note, add_folder

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('add', context_settings=CONTEXT_SETTINGS,
               short_help='Add notes and/or folders')
@click.option('-e', '--editor', 'editor', is_flag=True,
              help='Use buffer to enter note')
@click.option('-f', '--folder', 'folder', nargs=1,
              type=str, help='Create a folder with a given name')
@click.option('-n', '--note', 'note', is_flag=True,
              help='Add a new note entry')
@click.option('-p', '--path', 'path',
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              type=click.Path(writable=True),
              help='Specified path')
@click.argument('title', required=False, default='', type=str)
@click.argument('text', required=False, default='', type=str)
def add(editor, folder, note, path, title, text):
    """Add a new note to the notebook"""

    if folder and note:
        # Create the folder with the given path.
        # The path is the current directory by default.
        add_folder(folder, path=path)

        # In this case an extended path must be created
        # so the file is stored within the created directory
        file_path = os.path.join(path, folder)

        # Unreachable path created
        if not os.path.exists(file_path):
            raise click.UsageError('No such file or directory')

        added_note = add_note(editor=editor, title=title, text=text,
                              path=file_path)

        click.secho(added_note.to_string(), fg='green')

    elif folder:
        add_folder(folder, path=path)

    elif note:
        added_note = add_note(editor=editor, title=title, text=text,
                              path=path)

        click.secho(added_note.to_string(), fg='green')

    else:
        raise click.UsageError('Missing option')
