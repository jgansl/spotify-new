from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from os import getenv
load_dotenv()
usr = getenv('usr')
# TODO load
# scope = ",".join(["playlist-read-collaborative","playlist-modify-private","playlist-modify-public","playlist-read-private","user-read-playback-position","user-read-recently-played","user-top-read","user-modify-playback-state","user-read-currently-playing","user-read-playback-state","user-read-private","user-read-email","user-library-modify","user-library-read,","user-follow-modify","user-follow-read",])
scope = ",".join(
    [
        # Images
        "ugc-image-upload",
        # Listening History
        "user-read-recently-played",
        "user-read-playback-position",
        "user-top-read",
        # Playlists
        "playlist-modify-private",
        "playlist-read-collaborative",
        "playlist-read-private",
        "playlist-modify-public",
        # Playback
        "streaming",
        "app-remote-control",
        # Users
        "user-read-email",
        "user-read-private",
        # Follow
        "user-follow-read",
        "user-follow-modify",
        # Library
        "user-library-modify",
        "user-library-read",
        # Spotify Connect
        "user-read-currently-playing",
        "user-read-playback-state",
        "user-modify-playback-state",
    ]
)


auth = SpotifyOAuth(scope=scope)#,open_browser=False, cache_path="./.cache.json")
sp = Spotify(auth_manager=auth)
