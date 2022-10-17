import asyncio
import shutil

import click
from cinema_playout.config import LOCAL_CINEMA_PATH, LOCAL_MEDIA_PATH

from cinema_playout.loggerfactory import LoggerFactory
from cinema_playout.tasks import copy_hold_items, copy_playlist_items, remove_hold_items, remove_playlist_items

logger = LoggerFactory.get_logger("cli.storage")


@click.group()
@click.pass_context
def storage(ctx):
    pass


@storage.command()
def available():
    cinema_stat = shutil.disk_usage(LOCAL_CINEMA_PATH)
    percent_used = cinema_stat.used / cinema_stat.total
    click.echo(f"Cinema Remote Storage: {percent_used:.2%} Used")
    media_stat = shutil.disk_usage(LOCAL_MEDIA_PATH)
    percent_used = media_stat.used / media_stat.total
    click.echo(f"Media Local Storage: {percent_used:.2%} Used")


@storage.command()
def copy_to_local():
    asyncio.run(copy_playlist_items())
    asyncio.run(copy_hold_items())


@storage.command()
def remove_from_local():
    asyncio.run(remove_playlist_items())
    asyncio.run(remove_hold_items())
