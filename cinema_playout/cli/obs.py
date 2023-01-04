import click
import structlog

from cinema_playout.cli.utils import use_db_session
from cinema_playout.obs.playout import main_loop

logger = structlog.get_logger()


@click.group()
@click.pass_context
def obs(ctx):
    pass


@obs.command()
@use_db_session
def run(db_session):
    """Run OBS."""
    # TODO add tenacity for catch un expected exceptions
    main_loop()
