import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TMP_PATH_NAME  = "tmp"
TMP_PATH = os.path.join(SCRIPT_DIR, TMP_PATH_NAME)

GLB_NAME = "tmp.glb"
GLB_PATH = os.path.join(TMP_PATH, GLB_NAME)

COMMANDS_JSON_PATH = os.path.join(SCRIPT_DIR, "commands.json")

HTTP_PORT = 8001
SOCKET_PORT = 8000

with open(COMMANDS_JSON_PATH, 'r') as file:
    global SOCKET_COMMANDS_TO_ID, SOCKET_COMMANDS_FROM_ID
    SOCKET_COMMANDS_TO_ID = json.load(file)
    SOCKET_COMMANDS_FROM_ID = {v: k for k, v in SOCKET_COMMANDS_TO_ID.items()}
