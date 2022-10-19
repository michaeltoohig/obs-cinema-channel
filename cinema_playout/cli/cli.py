import shutil
import click

from cinema_playout.config import LOCAL_CINEMA_PATH, LOCAL_MEDIA_PATH

from .obs import obs as obs_cli
from .library import library as library_cli


@click.group()
@click.version_option()
def cli():
    "Cinema channel playout with OBS"


cli.add_command(obs_cli)
cli.add_command(library_cli)


@cli.command()
def storage():
    cinema_stat = shutil.disk_usage(LOCAL_CINEMA_PATH)
    percent_used = cinema_stat.used / cinema_stat.total
    click.echo(f"remote storage: {percent_used:.2%} Used")
    media_stat = shutil.disk_usage(LOCAL_MEDIA_PATH)
    percent_used = media_stat.used / media_stat.total
    click.echo(f"local storage: {percent_used:.2%} Used")
