import os

DEBUG = True if os.environ.get("DEBUG", "False").lower().startswith("t") else False

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DATABASE_URI = os.environ.get("DATABASE_URI")

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

# root path for cinema-playout script to access remote library files and local library files
REMOTE_LIBRARY_PATH = os.environ.get("REMOTE_LIBRARY_PATH")
LOCAL_LIBRARY_PATH = os.environ.get("LOCAL_LIBRARY_PATH")
# root path for OBS to access LOCAL_LIBRARY_PATH (OBS could be on separate machine from cinema-playout)
OBS_LIBRARY_PATH = os.environ.get("OBS_LIBRARY_PATH")

TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TG_TOKEN = os.environ.get("TG_TOKEN")
