import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEBUG = True if os.environ.get("DEBUG", "False").lower().startswith("t") else False

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DATABASE_URI = os.environ.get("DATABASE_URI")

CINEMA_SERVER_ID = int(os.environ.get("CINEMA_SERVER_ID"))

OBS_HOST = os.environ.get("OBS_HOST")
OBS_PORT = os.environ.get("OBS_PORT")
OBS_PASSWORD = os.environ.get("OBS_PASSWORD")

SERVER_ID = os.environ.get("SERVER_ID")

SCENE_FEATURE = os.environ.get("SCENE_FEATURE")
SOURCE_FEATURE = os.environ.get("SOURCE_FEATURE")
SOURCE_NOW_PLAYING = os.environ.get("SOURCE_NOW_PLAYING")
SOURCE_NEXT_PLAYING = os.environ.get("SOURCE_NEXT_PLAYING")
SCENE_HOLD = os.environ.get("SCENE_HOLD")
SOURCE_HOLD_VIDEO = os.environ.get("SOURCE_HOLD_VIDEO")
SOURCE_HOLD_MUSIC = os.environ.get("SOURCE_HOLD_MUSIC")

INFO_NOW_PLAYING = os.environ.get("INFO_NOW_PLAYING")
INFO_NEXT_PLAYING = os.environ.get("INFO_NEXT_PLAYING")

LOCAL_CINEMA_PATH = os.environ.get("LOCAL_CINEMA_PATH")
LOCAL_MEDIA_PATH = os.environ.get("LOCAL_MEDIA_PATH")
OBS_MEDIA_PATH = os.environ.get("OBS_MEDIA_PATH")

TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TG_TOKEN = os.environ.get("TG_TOKEN")
