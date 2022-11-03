import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = True if os.environ.get("DEBUG", "False").lower().startswith("t") else False

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DATABASE_URI = os.environ.get("DATABASE_URI")

OBS_HOST = os.environ.get("OBS_HOST")
OBS_PORT = os.environ.get("OBS_PORT")
OBS_PASSWORD = os.environ.get("OBS_PASSWORD")
OBS_SCREEN_X = int(os.environ.get("OBS_SCREEN_X", 1920))
OBS_SCREEN_Y = int(os.environ.get("OBS_SCREEN_Y", 1080))

SERVER_ID = os.environ.get("SERVER_ID", 0)  # for multiple instances sharing a database

SCENE_FEATURE = os.environ.get("SCENE_FEATURE", "feature")
SOURCE_FEATURE = os.environ.get("SOURCE_FEATURE", "feature-media")
SOURCE_NOW_PLAYING = os.environ.get("SOURCE_NOW_PLAYING", "info-now-playing")
SOURCE_NEXT_PLAYING = os.environ.get("SOURCE_NEXT_PLAYING", "info-next-playing")
SCENE_HOLD = os.environ.get("SCENE_HOLD", "hold")
SOURCE_HOLD_VIDEO = os.environ.get("SOURCE_HOLD_VIDEO", "hold-video")
SOURCE_HOLD_MUSIC = os.environ.get("SOURCE_HOLD_MUSIC", "hold-music")

INFO_NOW_PLAYING = os.environ.get("INFO_NOW_PLAYING", "now-playing.txt")
INFO_NEXT_PLAYING = os.environ.get("INFO_NEXT_PLAYING", "next-playing.txt")

DIRECTORY_HOLD_VIDEO = os.environ.get("DIRECTORY_HOLD_VIDEO", "hold-video")
DIRECTORY_HOLD_MUSIC = os.environ.get("DIRECTORY_HOLD_MUSIC", "hold-music")

# root path for SQL server to access remote library files
SQL_LIBRARY_PATH = os.environ.get("SQL_LIBRARY_PATH")
# root path for cinema-playout script to access remote library files and local library files
REMOTE_LIBRARY_PATH = os.environ.get("REMOTE_LIBRARY_PATH")
LOCAL_LIBRARY_PATH = os.environ.get("LOCAL_LIBRARY_PATH")
# root path for OBS to access LOCAL_LIBRARY_PATH (OBS could be on separate machine from cinema-playout)
OBS_LIBRARY_PATH = os.environ.get("OBS_LIBRARY_PATH")
# root path for remote hold items
REMOTE_HOLD_ROOT_PATH = str(Path(REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{SERVER_ID}")
REMOTE_HOLD_VIDEO_PATH = str(Path(REMOTE_HOLD_ROOT_PATH) / DIRECTORY_HOLD_VIDEO)
REMOTE_HOLD_MUSIC_PATH = str(Path(REMOTE_HOLD_ROOT_PATH) / DIRECTORY_HOLD_MUSIC)
LOCAL_HOLD_VIDEO_PATH = str(Path(LOCAL_LIBRARY_PATH) / DIRECTORY_HOLD_VIDEO)
LOCAL_HOLD_MUSIC_PATH = str(Path(LOCAL_LIBRARY_PATH) / DIRECTORY_HOLD_MUSIC)

LOCAL_LIBRARY_KEEP_FUTURE = int(os.environ.get("LOCAL_LIBRARY_KEEP_FUTURE", 1))
LOCAL_LIBRARY_KEEP_PAST = int(os.environ.get("LOCAL_LIBRARY_KEEP_PAST", 7))

TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TG_TOKEN = os.environ.get("TG_TOKEN")
