from spotipy.client import PLAYLIST, SAVED, TRACK#, Personal
from spotipy.exceptions import SpotifyException
from _oauth import sp, usr
from _personal import Personal


import os, re
from math import ceil
# import concurrent
from concurrent.futures import as_completed, ThreadPoolExecutor
from json import load, dump, dumps
from os import getenv, system
from pydash import flatten
from time import sleep
# import re #! reduce dep
from re import sub
import json

jprint = lambda x: print(json.dumps(x,indent=2))

mem = Personal(sp)
if __name__ == '__main__':
   
   # pnew = mem.pname('New')

   fn = 'heard.json'
   lst = set()
   # if os.path.exists(fn):
   with open(fn, 'r') as f:
      lst = set(json.load(f))
   # else:
   #    for p in owned:
   #       if p['name'] == 'New':
   #          continue
   #       lst.update(mem.get_track_ids(p))
   #    with open(fn, 'w') as f:
   #       json.dump(list(lst), f)
   #    exit()


   owned = [p for p in mem.playlists if usr == p['owner']['id']]
   for p in owned:
      lst.update(mem.get_track_ids(p))
   lst.update(mem.sids)

   radio_mixes = [p for p in mem.playlists if 'Mix' in p['name'] or 'Radio' in p['name']]
   for p in radio_mixes:
   # [
   #    'Chill',
   #    'Dance/Electronic',
   #    # 'Focus',
   #    'Folk & Acoustic',
   #    'Hip Hop',
   #    'House',
   #    'Indie',
   #    'Pop',
   #    'R&B',
   #    '2010s',
   #    '2000s',
   #    '90s',
   #    '80s',
   #    '70s',
   # ]:
      pn = re.sub('(Mix|Radio)', '', p['name'])
      # pn = re.sub('Radio', '', p['name'])
      # ref = mem.pname(f'{p} Mix')
      ref2 = mem.pname(f'{pn} New', description='.new')
      new_tracks = mem.diff(mem.get_track_ids(p), lst)
      print(pn, len(new_tracks))
      mem.move( None, ref2['id'], new_tracks)

      lst.update(new_tracks)
      with open(fn, 'w') as f:
         json.dump(list(lst), f)

      # remove track 60+ day old
      #TODO mem.move(
      # ref2['id'], 
      # None, 
      # [t for t in mem.get_track_ids(ref2) if t['added_at'] > date(-60 days)]
      # )
      # for t in mem.retrieve(TRACK, pid=ref2['id']):
      #    datetime.strptime('Y-m-d', t['added_at'] datetime.strptime('Y-m-d', datetimte.now())

