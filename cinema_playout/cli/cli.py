import logging
import shutil

import click

from cinema_playout import config
from cinema_playout.logging import configure_logger

from .library import library as library_cli
from .obs import obs as obs_cli


@click.group()
@click.version_option()
@click.option("--strict", is_flag=True, default=False, help="Format log messages appropriate for production use.")
@click.option("-v", "--verbose", count=True, help="Show more log messages.")
def cli(strict, verbose):
    """Cinema channel playout with OBS"""
    log_levels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    idx = min(verbose, 2)
    level = log_levels[idx]
    configure_logger(strict, level)


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
