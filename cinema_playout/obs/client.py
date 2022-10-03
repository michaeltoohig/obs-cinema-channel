"""
OBS Websocket Client
DOCS: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
DOCS 4.x: https://github.com/obsproject/obs-websocket/blob/4.x-compat/docs/generated/protocol.md
"""

import asyncio
from pathlib import Path

import simpleobsws

from cinema_playout.config import (
    OBS_HOST,
    OBS_PASSWORD,
    OBS_PORT,
    SCENE_FEATURE,
    SCENE_HOLD,
    SOURCE_FEATURE,
    SOURCE_HOLD_MUSIC,
    SOURCE_HOLD_VIDEO,
    SOURCE_NEXT_PLAYING,
    SOURCE_NOW_PLAYING,
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

    async def play_hold(self):
        """
        Switch to hold scene and queue up all video backgrounds and music.
        """
        logger.debug("Play hold")
        await self.request("SetCurrentScene", {"scene-name": SCENE_HOLD})
        vids = Path("/mnt/cinema-media/CinemaPlayout/server-1/hold-videos").glob("*")
        vids = [
            {"hidden": False, "selected": False, "value": "Y:/" + str(v.relative_to("/mnt/cinema-media"))} for v in vids
        ]
        await self.request("SetSourceSettings", {"sourceName": SOURCE_HOLD_VIDEO, "sourceSettings": {"playlist": vids}})
        await self.request("PlayPauseMedia", {"sourceName": SOURCE_HOLD_VIDEO, "playPause": False})  # play

        music = Path("/mnt/cinema-media/CinemaPlayout/server-1/hold-music").glob("*")
        music = [
            {"hidden": False, "selected": False, "value": "Y:/" + str(m.relative_to("/mnt/cinema-media"))}
            for m in music
        ]
        await self.request(
            "SetSourceSettings", {"sourceName": SOURCE_HOLD_MUSIC, "sourceSettings": {"playlist": music}}
        )
        await self.request("PlayPauseMedia", {"sourceName": SOURCE_HOLD_MUSIC, "playPause": False})  # play

    async def show_current_feature_name(self, visible: bool):
        """
        Show current feature name on feature scene.
        """
        await self.request(
            "SetSceneItemProperties", {"scene-name": SCENE_FEATURE, "item": SOURCE_NOW_PLAYING, "visible": visible}
        )

    async def show_next_feature_name(self, visible: bool):
        """
        Show next feature name on feature scene.
        """
        await self.request(
            "SetSceneItemProperties", {"scene-name": SCENE_FEATURE, "item": SOURCE_NEXT_PLAYING, "visible": visible}
        )
