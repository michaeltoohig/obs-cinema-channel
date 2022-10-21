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
def copy():
    """Copy remote copies to local storage ready for playout."""
    asyncio.run(copy_playlist_items())
    asyncio.run(copy_hold_items())


@library.command()
def free():
    """Free space on local storage by removing old items."""
    asyncio.run(remove_playlist_items())
    asyncio.run(remove_hold_items())


@library.command()
def check():
    """Check files exist where they should on remote and local storage."""
    # TODO check all features are available in library and find incorrect file locations
    pass
