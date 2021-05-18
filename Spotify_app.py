import spotipy
import os
import sys
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get username
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'


