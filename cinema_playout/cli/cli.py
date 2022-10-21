import shutil
import click

from cinema_playout import config

from .obs import obs as obs_cli
from .library import library as library_cli


@click.group()
@click.version_option()
def cli():
    """Cinema channel playout with OBS"""


cli.add_command(obs_cli)
cli.add_command(library_cli)


@cli.command()
def storage():
    cinema_stat = shutil.disk_usage(config.REMOTE_LIBRARY_PATH)
    percent_used = cinema_stat.used / cinema_stat.total
    click.echo(f"remote storage: {percent_used:.2%} Used")
    media_stat = shutil.disk_usage(config.LOCAL_LIBRARY_PATH)
    percent_used = media_stat.used / media_stat.total
    click.echo(f"local storage: {percent_used:.2%} Used")
