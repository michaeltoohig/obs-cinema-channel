import asyncio

import click

from cinema_playout.cli.utils import coro, use_db_session
from cinema_playout.database.models import Feature
from cinema_playout.loggerfactory import LoggerFactory
from cinema_playout.obs.client import OBSClient
from cinema_playout.obs.playout import main_loop

logger = LoggerFactory.get_logger("obs")


@click.group()
@click.pass_context
def obs(ctx):
    pass


# async def playout_loop(c):
#     res = await c.request("GetSourceActive", {"sourceName": "vlc-feature"})
#     print(res)
#     res = await c.request("GetSourceSettings", {"sourceName": "vlc-feature"})
#     print(res)


async def on_event(eventType, eventData):
    print("New event! Type: {} | Raw Data: {}".format(eventType, eventData))  # Print


async def test(client):
    uri = "C:/Users/Michael/Videos/Made For 1NOMO/AWU22-1/AdvertiseWithUs-2022(b).mp4"
    # resp = await client.request(
    #     "SetSourceSettings", {"sourceName": "vlc-feature", "sourceSettings": {"local_file": uri}}
    # )
    resp = await client.request("GetSceneItemProperties", {"item": "vlc-feature"})
    print(resp)


@obs.command()
@use_db_session
def run(db_session):
    """Run OBS."""
    # TODO add tenacity for catch un expected exceptions
    main_loop()

    # loop = asyncio.get_event_loop()
    # client = OBSClient(loop=loop)
    # loop.run_until_complete(client.connect())
    # # client.client.register_event_callback(on_event)
    # loop.run_until_complete(test(client))
    # # loop.run_forever()
