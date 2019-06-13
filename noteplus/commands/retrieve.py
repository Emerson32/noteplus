# retrieve.py - Returns a list of note entries within the database

import click
import os

from noteplus.commands.basis import NoteBook


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('retrieve', context_settings=CONTEXT_SETTINGS,
               short_help='retrieve note entries')
@click.option('-a', '--all', 'all_notes', is_flag=True,
              help='retrieve all note entries')
@click.option('-l', '--less', 'less', is_flag=True,
              help='show note(s) by using a pager')
@click.option('-t', '--title', 'title', nargs=1, type=str,
              help='retrieve a note based on its title')
@click.option('-n', '--note', 'note', nargs=1, type=str,
              help='retrieve a note based on the note')
@click.option('-nb', '--notebook', 'notebook', nargs=1,
              type=str, default='notes.db',
              show_default=True,
              help='Name of notebook file')
@click.option('-p', '--path', 'path', nargs=1,
              type=click.Path(readable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='Specific directory of note retrieval')
def retrieve(all_notes, less, title, note, notebook, path):
    """Retrieve a note from the notebook"""

    if not os.path.isfile(os.path.join(path, notebook)):
        raise click.UsageError("Notes file named "
                               + "\'" + notebook + "\', does not exist"
                               + " within the provided path")

    if not os.path.exists(path):
        raise click.UsageError('No such file or directory')

    target_nb = NoteBook(path=path, file_name=notebook)

    if all_notes:
        os.chdir(path)

        results = target_nb.retrieve_all()

        # Less pager selected
        if less:
            lines = ''

            # Build the lines to be displayed
            for item in results:
                lines += "Title: " + item[0] + \
                         "\nNote: " + item[1] + \
                         "\nTime: " + item[2] + "\n\n"

            click.echo_via_pager(lines)

        else:
            for item in results:
                click.echo()
                click.echo("Title: ", nl=False)
                click.secho(item[0], bold=True)
                click.echo("Note: ", nl=False)
                click.secho(item[1], bold=True)
                click.echo("Time: ", nl=False)
                click.secho(item[2], bold=True)

    elif title:
        os.chdir(path)

        results = target_nb.retrieve_by_title(title=title)
        for item in results:
            click.echo()
            click.echo("Title: ", nl=False)
            click.secho(item[0], bold=True)
            click.echo("Note: ", nl=False)
            click.secho(item[1], bold=True)
            click.echo("Time: ", nl=False)
            click.secho(item[2], bold=True)

    elif note:
        os.chdir(path)

        results = target_nb.retrieve_by_note(note=note)

        for item in results:
            click.echo()
            click.echo("Title: ", nl=False)
            click.secho(item[0], bold=True)
            click.echo("Note: ", nl=False)
            click.secho(item[1], bold=True)
            click.echo("Time: ", nl=False)
            click.secho(item[2], bold=True)

    else:
        raise click.UsageError('Missing necessary retrieval option')
