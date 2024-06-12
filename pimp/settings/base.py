from pathlib import Path
import json

#### Define the file path ####
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR/'static'
CONFIG_FILE = BASE_DIR/'config.json'

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

BASE_THEME = config['THEME']
INITIAL_DIR = config['INITIAL_DIR']
INITIAL_IMAGE = config['INITIAL_IMAGE']
LAST_IMAGE = BASE_DIR/config['LAST_IMAGE']
PREVIEW_IMAGE = BASE_DIR/config['PREVIEW_IMAGE']
# Define the parameters
MAIN_WIN_TITLE = "PIMP"
MAIN_WIN_SIZE = (900,600)
# shortcut_key_page_size = "700x600"

# LOGO_ICO = str(STATIC_DIR/'image/logo.ico')
# LOGO_ICO = str(STATIC_DIR/'image/logo.png')
LOGO = str(STATIC_DIR/'image/logo.png')

print("BASE Setting")