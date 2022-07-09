from spotipy.client import PLAYLIST, SAVED, TRACK#, Personal
from spotipy.exceptions import SpotifyException
from _oauth import sp, usr
from _personal import Personal


import os
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
tags = ['.personal','memories']
channels = { #!
   # monday 'Troy + Jesse': SAVED,
   'On Repeat': 'Cache'
}
mem = Personal(sp)
def backup():
   global mem
   # fn = "data/backup.json"
   # data = {
   #    'liked': mem.sids
   # }
   # if os.path.exists(fn):
   #    try:
   #       with open(fn, 'r') as f:
   #          json.load(f)
   #    except:
   #       exit()
   owned = [p for p in mem.playlists if p['owner']['id'] == usr]
   for p in owned:
      # data[p['id']] = {
      #    'name': p['name'],
      #    'description': p['description'],
      #    'tracks': mem.get_track_ids(p)
      # }
      # with open(fn, 'w') as f:
      #    json.dump(data,f,indent=2)
      sp.user_playlist_unfollow(usr,p['id'])
   return

def weekday():
   def monday():
      return
   return

if __name__ == '__main__':
   # backup()
   # mem.move(SAVED, None, mem.sids)
   # sp.user_playlist_follow_playlist(usr, '5rhssu3GmdykcTiJzXbPPD')

   musc = mem.pname('_')
   nost = mem.pname('Nostalgia')
   cach = mem.pname('Cache')

   owned = [p for p in mem.playlists if usr == p['owner']['id']]
   memories = [p for p in mem.playlists if '.memories' in p['description']]

   for p in [*channels]: #! saved playlist generated
      ref = mem.pname(p)
      lst = None
      if channels[p] == SAVED:
         lst = mem.get_track_ids(ref)
         lst = mem.diff(mem.get_track_ids(ref), mem.sids)
         if len(lst):
            mem.move(None, SAVED, lst) #! add/remove toggling
      else:
         ref2 = mem.pname(channels[p])
         lst = mem.diff(mem.get_track_ids(ref), mem.get_track_ids(ref2))
         if len(lst):
            mem.move(
               None,
               ref2['id'],
               lst
            )
      print(p, len(lst))

   for p in [
      'Chill',
      'Dance/Electronic',
      # 'Focus',
      'Folk & Acoustic',
      'Hip Hop',
      'House',
      'Indie',
      'Pop',
      'R&B',
      '2010s',
      '2000s',
      '90s',
      '80s',
      '70s',
   ]:
      ref = mem.pname(f'{p} Mix')
      ref2 = mem.pname(f'{p} Collection', description='.personal .genre')
      lst = mem.diff(mem.intersect( #! remove coll from saved?
               mem.get_track_ids(ref),
               mem.sids
            ), mem.get_track_ids(ref2))
      print(p, len(lst))
      mem.move( None, ref2['id'], lst)
      mem.move( SAVED, None, mem.intersect(mem.sids, ref2) )
   
   # remove nostalgia from saved
   lst = mem.intersect(mem.sids, mem.get_track_ids(nost))
   print('NOST<-SAVED', len(lst))
   mem.move(SAVED, None, lst)
   
   lst = mem.intersect(mem.sids, mem.get_track_ids(mem.pname('Cache')))
   mem.move(SAVED, None, lst)

   # remove memories from all
   # cache removal; rmeove genre coll from nost
   #programatic hidden -> supabase
   #! in genre coll playlist attribute tuning

   # remove memories from all
   tmp = {}
   for mp in memories:
      tmp[mp['id']] = mem.get_track_ids(mp)
      mem.move(SAVED, None, tmp[mp['id']])
   for p in owned:
      for mp in memories:
         if '.memories' in p['description']:
            continue
         if p['id'] not in [*tmp]:
            tmp[p['id']] = mem.get_track_ids(p)
         mem.move(p['id'], None, mem.intersect(
            tmp[p['id']],
            tmp[mp['id']],
         ))
