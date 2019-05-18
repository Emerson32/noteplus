import click


@click.command()
@click.option('--name', 'name', default='Steve', help='Simple greeting message.')
def greeting(name):
    click.echo("Hello %s!" % name)

