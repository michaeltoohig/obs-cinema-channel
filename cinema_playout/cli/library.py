import click
import structlog

from cinema_playout.tasks import copy_hold_items, copy_playlist_items, remove_hold_items, remove_playlist_items

logger = structlog.get_logger()


@click.group()
@click.pass_context
def library(ctx):
    pass


@library.command()
def copy():
    """Copy remote copies to local storage ready for playout."""
    copy_playlist_items()
    copy_hold_items()


@library.command()
def free():
    """Free space on local storage by removing old items."""
    remove_playlist_items()
    remove_hold_items()


@library.command()
def check():
    """Check files exist where they should on remote and local storage."""
    # TODO check all features are available in library and find incorrect file locations
    pass
