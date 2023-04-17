import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import os
from dotenv import load_dotenv
from pathlib import Path 
import logging

"""Set environment variables"""
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
#Environemnt variables that contains the user credentials to access Spotify API 
"""input user name"""
username = os.getenv("user_name")
cid = os.getenv("client_id")
secret = os.getenv("client_secret")
redirect = os.getenv("redirect_uri")
playlist_name = os.getenv("playlist_name")

"""Get artists"""
file = open("data/artists.txt","r") 
u_artists = [x.replace("\n", "") for x in file.readlines()]
file.close() 

"""Get Spotify Access"""
"""create a log for errors"""
logger = logging.getLogger(playlist_name.lower().replace(" ", "_"))
hdlr = logging.FileHandler('playlists.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

"""get token for user authentication"""
token = util.prompt_for_user_token(username, 
                                   scope='playlist-modify-private,playlist-modify-public', 
                                   client_id = cid, 
                                   client_secret=secret,
                                   redirect_uri=redirect)
"""get access from spotify"""
"""establish connection"""
#sp = spotipy.Spotify()
#client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(auth=token)
logger.info("got spotify access info")
#establish access
logger.info("got spotify access")

"""find an aritist's top spotify songs uri(s) based on the artist's spotify id"""
def get_top_songs_for_artist(artist, song_count=5):
    """find an aritist's top spotify songs uri(s) based on the artist's spotify id.
    Args:
        artist (str): name of an artist
        song_count (int): number of top songs you want to find
    Returns:
        song_ids (list): top n song uris
    """
    song_ids = []
    try:
        t = sp.search("artist:{}".format(artist), limit = 1)
        artist_id = t['tracks']['items'][0]['artists'][0]['id']
        artist_top_tracks = sp.artist_top_tracks(artist_id)
        artist_top_tracks_length = len(artist_top_tracks['tracks'])
        for i in range(0, artist_top_tracks_length if song_count > artist_top_tracks_length else song_count ):
            song_ids.append(artist_top_tracks['tracks'][i]['uri'])
            logger.info(str(len(song_ids)) + ' songs found - ' + artist)
    except:
        logger.info('Artist not found - ' + artist)
    return song_ids


"""get playlist information, create one if not exists"""
playlists = sp.user_playlists(username)

for p in playlists['items']:
    if p['name'] == playlist_name:
        p_id = p['id']
        
if not 'p_id' in globals():
    sp.user_playlist_create(username, playlist_name)
    for p in playlists['items']:
        if p['name'] == playlist_name:
            p_id = p['id']

"""Get existing songs if there are"""
e_lst = sp.user_playlist(username, p_id)
if len(e_lst['tracks']['items']) > 0:
    exist_song_ids = []
    for item in e_lst['tracks']['items']:
        exist_song_ids.append(item['track']['uri'])

"""Add top n songs"""
api_track_add_limit = 100
all_track_ids = []
for current_artist in u_artists:
    top_song_limit_per_artist = 4
    top_artist_songs = get_top_songs_for_artist(current_artist, top_song_limit_per_artist)
    if 'exist_song_ids' in globals():
        all_track_ids.extend([x for x in top_artist_songs if x not in exist_song_ids])
    else:
        all_track_ids.extend(top_artist_songs)

"""Add songs to the api limit (100)"""
all_songs_len = len(all_track_ids)
sp.user_playlist_add_tracks(user=username, 
                            playlist_id=p_id, 
                            tracks=all_track_ids[:min(api_track_add_limit, all_songs_len)])
logger.info("Finished adding {} songs.".format(min(api_track_add_limit, all_songs_len)))
