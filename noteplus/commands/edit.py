# edit.py - Edit the contents of a note entry
import click
import os

from noteplus.commands.operations import rename_title, edit_note

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('edit', context_settings=CONTEXT_SETTINGS,
               short_help='edit a note')
@click.option('--rename', 'rename_type',
              type=click.Choice(['note', 'folder']),
              help='rename a note or folder')
@click.option('-n', '--note', 'note',
              nargs=1, type=str,
              help='edit the text of a given note entry (arg = title)')
@click.argument('old_title', required=False, type=str)
@click.argument('new_title', required=False, type=str)
def edit(rename_type, note, old_title, new_title):
    """Make changes to a note or folder"""
    if rename_type:
        if not (old_title or new_title):
            raise click.UsageError('Missing title argument')

        if rename_type == 'folder':
            os.rename(old_title, new_title)
            old_dir = os.path.join(os.getcwd(), old_title)
            new_dir = os.path.join(os.getcwd(), new_title)

            click.echo("Renamed ",  nl=False)
            click.secho(old_dir, bold=True, fg='white', nl=False)
            click.echo(" to ", nl=False)
            click.secho(new_dir, bold=True, fg='green')

        else:
            rename_title(old_title=old_title, new_title=new_title)
            old_file = os.path.join(os.getcwd(), old_title)
            new_file = os.path.join(os.getcwd(), new_title)

            click.echo("Renamed ",  nl=False)
            click.secho(old_file, bold=True, fg='white', nl=False)
            click.echo(" to ", nl=False)
            click.secho(new_file, bold=True, fg='green')

    elif note:
        edit_note(note_title=note)
