import asyncio

import click

from cinema_playout.loggerfactory import LoggerFactory
from cinema_playout.tasks import copy_hold_items, copy_playlist_items, remove_hold_items, remove_playlist_items

logger = LoggerFactory.get_logger("cli.library")


@click.group()
@click.pass_context
def library(ctx):
    pass


@library.command()
def copy_to_local():
    asyncio.run(copy_playlist_items())
    asyncio.run(copy_hold_items())


@library.command()
def remove_from_local():
    asyncio.run(remove_playlist_items())
    asyncio.run(remove_hold_items())


@library.command()
def check():
    # TODO check all features are available in library and find incorrect file locations
    pass
