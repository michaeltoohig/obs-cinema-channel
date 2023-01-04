"""
OBS Websocket Client
DOCS: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
DOCS 4.x: https://github.com/obsproject/obs-websocket/blob/4.x-compat/docs/generated/protocol.md
"""

import asyncio
from pathlib import Path

import simpleobsws
import structlog

from cinema_playout import config
from cinema_playout.obs.exceptions import OBSConnectionError

logger = structlog.get_logger()


class OBSClient:
    def __init__(self, loop):
        # self.URL = f"ws://{config.OBS_HOST}:{config.OBS_PORT}"
        # self.client = simpleobsws.WebSocketClient(self.URL, config.OBS_PASSWORD)
        self.client = simpleobsws.obsws(
            host=config.OBS_HOST, port=config.OBS_PORT, password=config.OBS_PASSWORD, loop=loop
        )

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

    async def play_feature(self, fp: Path, offset: int = None):
        """
        Switch to main feature scene and play feature.
        """
        logger.debug(f"Playing feature {fp}")
        await self.request("SetCurrentScene", {"scene-name": config.SCENE_FEATURE})
        await self.request(
            "SetSourceSettings",
            {"sourceName": config.SOURCE_FEATURE, "sourceSettings": {"playlist": [{"value": str(fp)}]}},
        )
        if offset:
            logger.debug(f"SetMediaTime offset {offset}")
            await asyncio.sleep(1)
            await self.request("SetMediaTime", {"sourceName": config.SOURCE_FEATURE, "timestamp": offset})
        await self.request(
            "SetSceneItemProperties",
            {
                "scene-name": config.SCENE_FEATURE,
                "item": config.SOURCE_FEATURE,
                "position": {"x": 0, "y": 0},
                "bounds": {"x": config.OBS_SCREEN_X, "y": config.OBS_SCREEN_Y, "type": "OBS_BOUNDS_MAX_ONLY"},
                "scale": {"x": 4, "y": 4, "filter": "OBS_SCALE_AREA"},
            },
        )

    async def play_hold(self):
        """
        Switch to hold scene and queue up all video backgrounds and music.
        """
        logger.debug("Playing hold scene")
        await self.request("SetCurrentScene", {"scene-name": config.SCENE_HOLD})

    async def update_hold_media(self):
        """Set hold scene media content."""
        vids = Path(config.LOCAL_HOLD_VIDEO_PATH).glob("*")
        vids = [
            {
                "hidden": False,
                "selected": False,
                "value": str(Path(config.OBS_LIBRARY_PATH) / v.relative_to(config.LOCAL_LIBRARY_PATH)),
            }
            for v in vids
        ]
        await self.request(
            "SetSourceSettings", {"sourceName": config.SOURCE_HOLD_VIDEO, "sourceSettings": {"playlist": vids}}
        )
        music = Path(config.LOCAL_HOLD_MUSIC_PATH).glob("*")
        music = [
            {
                "hidden": False,
                "selected": False,
                "value": str(Path(config.OBS_LIBRARY_PATH) / m.relative_to(config.LOCAL_LIBRARY_PATH)),
            }
            for m in music
        ]

    async def show_current_feature_name(self, visible: bool):
        """
        Show current feature name on feature scene.
        """
        logger.debug("Showing current feature name")
        await self.request(
            "SetSceneItemProperties",
            {"scene-name": config.SCENE_FEATURE, "item": config.SOURCE_NOW_PLAYING, "visible": visible},
        )

    async def show_next_feature_name(self, visible: bool):
        """
        Show next feature name on feature scene.
        """
        logger.debug("Showing next feature name")
        await self.request(
            "SetSceneItemProperties",
            {"scene-name": config.SCENE_FEATURE, "item": config.SOURCE_NEXT_PLAYING, "visible": visible},
        )
