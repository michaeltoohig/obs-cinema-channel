import click

from .obs import obs as obs_cli


@click.group()
@click.version_option()
def cli():
    "Cinema channel playout with OBS"


cli.add_command(obs_cli)
