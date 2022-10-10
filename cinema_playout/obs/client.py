"""
OBS Websocket Client
DOCS: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
DOCS 4.x: https://github.com/obsproject/obs-websocket/blob/4.x-compat/docs/generated/protocol.md
"""

import asyncio
from pathlib import Path

import simpleobsws

from cinema_playout.config import (
    OBS_CINEMA_PATH,
    OBS_HOST,
    OBS_PASSWORD,
    OBS_PORT,
    SCENE_FEATURE,
    SCENE_HOLD,
    SERVER_ID,
    SOURCE_FEATURE,
    SOURCE_HOLD_MUSIC,
    SOURCE_HOLD_VIDEO,
    SOURCE_NEXT_PLAYING,
    SOURCE_NOW_PLAYING,
    LOCAL_CINEMA_PATH,
)
from cinema_playout.loggerfactory import LoggerFactory
from cinema_playout.obs.exceptions import OBSConnectionError

logger = LoggerFactory.get_logger("obs.client")


class OBSClient:
    def __init__(self, loop):
        # self.URL = f"ws://{OBS_HOST}:{OBS_PORT}"
        # self.client = simpleobsws.WebSocketClient(self.URL, OBS_PASSWORD)
        self.client = simpleobsws.obsws(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, loop=loop)

    async def __aenter__(self):
        try:
            await self.connect()
        except OBSConnectionError:
            await self.disconnect()
            raise

    async def __aexit__(self, *args, **kwargs):
        self.disconnect()

    async def connect(self):
        """
        Connect to OBS websocket server.
        """
        logger.debug("OBSClient connecting")
        try:
            await self.client.connect()
            # await self.client.wait_until_identified()
            return True
        except Exception:
            raise OBSConnectionError("OBSClient connection failure")

    async def disconnect(self):
        logger.debug("OBSClient disconnecting")
        await self.client.disconnect()

    async def request(self, name, data=None):
        """
        Perform a raw request to the OBS instance.
        """
        # request = simpleobsws.Request(name, requestData=data)  # Build a Request object
        # ret = await self.client.call(request)
        # if ret.ok():
        #     print("Request succeeded! Response data: {}".format(ret.responseData))
        # return ret
        ret = await self.client.call(name, data)
        return ret

    async def play_feature(self, fp: str, offset: int = None):
        """
        Switch to main feature scene and play feature.
        """
        logger.debug(f"Playing feature {fp}")
        await self.request("SetCurrentScene", {"scene-name": SCENE_FEATURE})
        await self.request(
            "SetSourceSettings", {"sourceName": SOURCE_FEATURE, "sourceSettings": {"playlist": [{"value": fp}]}}
        )
        if offset:
            logger.debug(f"SetMediaTime offset {offset}")
            await asyncio.sleep(1)
            await self.request("SetMediaTime", {"sourceName": SOURCE_FEATURE, "timestamp": offset})
        await self.request(
            "SetSceneItemProperties",
            {
                "scene-name": SCENE_FEATURE,
                "item": SOURCE_FEATURE,
                "position": {"x": 0, "y": 0},
                "bounds": {"x": 1920, "y": 1080, "type": "OBS_BOUNDS_MAX_ONLY"},
                "scale": {"x": 4, "y": 4, "filter": "OBS_SCALE_AREA"},
            },
        )

    async def update_hold_media(self):
        """Set hold scene media content."""
        vids = (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-videos").glob("*")
        vids = [
            {
                "hidden": False,
                "selected": False,
                "value": OBS_CINEMA_PATH + str(v.relative_to(LOCAL_CINEMA_PATH)),
            }
            for v in vids
        ]
        await self.request("SetSourceSettings", {"sourceName": SOURCE_HOLD_VIDEO, "sourceSettings": {"playlist": vids}})
        music = (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-music").glob("*")
        music = [
            {
                "hidden": False,
                "selected": False,
                "value": OBS_CINEMA_PATH + str(m.relative_to(LOCAL_CINEMA_PATH)),
            }
            for m in music
        ]
        await self.request(
            "SetSourceSettings", {"sourceName": SOURCE_HOLD_MUSIC, "sourceSettings": {"playlist": music}}
        )
        await self.request("PlayPauseMedia", {"sourceName": SOURCE_HOLD_VIDEO, "playPause": False})  # play
        await self.request("PlayPauseMedia", {"sourceName": SOURCE_HOLD_MUSIC, "playPause": False})  # play

    async def play_hold(self):
        """
        Switch to hold scene and queue up all video backgrounds and music.
        """
        logger.debug("Playing hold scene")
        await self.request("SetCurrentScene", {"scene-name": SCENE_HOLD})

    async def show_current_feature_name(self, visible: bool):
        """
        Show current feature name on feature scene.
        """
        logger.debug("Showing current feature name")
        await self.request(
            "SetSceneItemProperties", {"scene-name": SCENE_FEATURE, "item": SOURCE_NOW_PLAYING, "visible": visible}
        )

    async def show_next_feature_name(self, visible: bool):
        """
        Show next feature name on feature scene.
        """
        logger.debug("Showing next feature name")
        await self.request(
            "SetSceneItemProperties", {"scene-name": SCENE_FEATURE, "item": SOURCE_NEXT_PLAYING, "visible": visible}
        )
