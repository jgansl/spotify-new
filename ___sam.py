# import unittesting
# improt mpytest

from spotipy.client import PLAYLIST, SAVED, TRACK#, Personal
from spotipy.exceptions import SpotifyException
from _oauth import sp, usr

import concurrent
from math import ceil
from concurrent.futures import as_completed, ThreadPoolExecutor
from json import load, dump, dumps
from os import getenv, system
from pydash import flatten
from time import sleep
# import re #! reduce dep
import json


jprint = lambda x: print(json.dumps(x,indent=2))

class SAM(object):
   def __init__(self, client=None):
      # self.sp = client
      # if not client:
      #    self.sp = sp
      self.playlists = self.retrieve(PLAYLIST)
      self.saved = self.retrieve(SAVED) # lazy init
      self.sids = [s['track']['id'] for s in self.saved]
      self.mem = {}
   
   def _paginate(self, func, *args, **kwargs):
    
      data = []
      lim = 50  # ! if not lim
      pack = {}
      if "lim" in kwargs.keys():
         lim = kwargs["lim"]
      pack["limit"] = lim
      if "pid" in kwargs.keys():
         pack['user'] = usr
         pack['playlist_id'] = kwargs["pid"]

      # init
      res = func(**pack)
      total = res["total"]
      data = res['items']

      if total > lim:
         with ThreadPoolExecutor(max_workers=15) as executor:
               future_res = {
                  executor.submit(func, offset=i*lim, **pack): i for i in range(1, ceil(total / lim))
               }
               for future in as_completed(future_res):
                  data.extend(future.result()["items"])

         # sort
      return data

   def retrieve(self, typ, pid=None, *args, **kwargs,):  # !TIDS
      # global sp, cache  # !cache
      mp = {
         PLAYLIST: sp.current_user_playlists,
         SAVED: sp.current_user_saved_tracks,
         TRACK: sp.user_playlist_tracks,
      }

      if typ.lower().strip() == SAVED:
         # if 'saved' not in [*mem]:
         #     mem['saved'] = {"name": "saved", "tracks": None, "tids": None}
         # if mem['saved']['tracks']:
         #     return mem['saved']['tracks']
         # else:
         res = self._paginate(sp.current_user_saved_tracks, *args, **kwargs)
         for t in res:
            del t['track']['album']['available_markets']
            del t['track']['available_markets']
         return res
      elif typ.lower().strip() == PLAYLIST:
         res = self._paginate(sp.current_user_playlists, *args, **kwargs)
         # id & type ++> pid and sid same?
         #! ? name, history, keywords..

         return res
      elif typ.lower().strip() == TRACK:
         res = self._paginate(sp.user_playlist_tracks, pid=pid,
                           *args, user=usr, **kwargs)
         for t in res:
            try:
               del t['track']['album']['available_markets']
               del t['track']['available_markets']
            except: pass
         return res
      # elif typ.lower().strip() == ARTIST_ALBUMS:  # multiple artiusts?
      #    pass
   
   def move(self, src, dst, items=[], owned=True, limit=50):
      def parallel(src, dst, items=[], owned=True):
         # print(dst)
         if dst:
            if dst.lower() == SAVED:
               try:
                  snpsht = sp.current_user_saved_tracks_add(tracks=items)
               except SpotifyException:
                  for i in items:
                     try:
                        snpsht = sp.current_user_saved_tracks_add(tracks=[i])
                     except: #!
                        pass
            else:
               try:
                  snpsht = sp.user_playlist_add_tracks(
                     user=usr, playlist_id=dst, tracks=items
                  )
                  if snpsht:
                     pass  # log(0, snpsht)  # log(0, err)
               # non existent IDs - spotipy.client.SpotifyException, requests.exceptions.HTTPError
               except SpotifyException:
                  grace = False
                  for i in items:
                     try:
                        snpsht = sp.user_playlist_add_tracks(
                           user=usr, playlist_id=dst, tracks=[i]
                        )
                        if snpsht:
                           pass  # print("ADDING", snpsht)
                     except SpotifyException:
                        if not grace:
                           #!log(1, "Skipped adding track..")
                           pass
                        grace = True
                        continue

         # src removal
         if src:
            if src.lower() == SAVED:
               snpsht = sp.current_user_saved_tracks_delete(tracks=items)
            elif src:
               if owned:
                  # TODO internally check that it is a list of string ids
                  snpsht = sp.user_playlist_remove_all_occurrences_of_tracks(
                     user=usr, playlist_id=src, tracks=items, snapshot_id=None
                  )
                  # sp.user_playlist_remove_tracks(user=usr, playlist_id=lst[i]['pid'], tracks=t)
                  # if snpsht:
                  #    print("REMOVE", snpsht)
         return
      #! AttributeError: 'dict' object has no attribute 'lower' -> ID, check if dict
      if type(src) == 'dict':
         src = src['id']
      if type(dst) == 'dict':
         dst = dst['id']
      if src and SAVED in src.lower():
         src = SAVED
      if dst and SAVED in dst.lower():
         dst = SAVED
      # jprint(items)
      if not len(items):
         return

      executor = ThreadPoolExecutor(max_workers=7)
      reqs = len(items) // limit
      # print(reqs)

      for i in range(reqs):
         print("Submitted", str(i))
         # executor.submit(parallel, src, dst,
         #                   items[i * 50: i * 50 + 50], owned=owned)
         parallel(src, dst, items[i * 50: i * 50 + 50], owned=owned)
      # executor.submit(parallel, src, dst,
      #                items[reqs * 50: len(items)], owned=owned)
      parallel(src, dst, items[reqs * 50: len(items)], owned=owned)
      # try:
      self.saved = self.retrieve(SAVED) # lazy init
      self.sids = [s['track']['id'] for s in self.saved]
      # print('SAVED', len(self.sids))
         # self.saved = sp.retrieve(SAVED)
         # self.sids = [s['track']['id'] for s in self.saved]
      # except:
      #    print('sids not updated')
      return 
   
   def tids(self, tdicts: list) -> list:
      return

   def sids(self):
      return
   
   def pname(self, name: str, cont=None, refreshed=False, equal=True, create=True, ownly=False, description='') -> dict:  # !
      # global playlists
      if equal:
         res = [p for p in self.playlists if name.lower() == p['name'].lower()
                  ]  # new vs newaritst
         if ownly:
            res = [p for p in res if p['owner']['id'] == usr]
      else:
         res = [p for p in self.playlists if name.lower() in p['name'].lower()]  # dm
         if ownly:
               res = [p for p in res if p['owner']['id'] == usr]
      if not cont and len(res) > 1:
         for p in res:
               print(p['name'])
         # !
         response = input(
            f'multiple playlist that contain {name}. continue? index0?').strip()
         if response.lower() == 'y':
            return res[0]
         if response.isdigit():
            print('using ' + res[int(response)]['name'])
            sleep(1.5)
            return res[int(response)]

      elif len(res):
         return res[0]
      # elif not refreshed:
      #     playlists = retrieve(PLAYLIST)
      #     return pname(name, refreshed=True)
      elif create:
         print('Creating')
         res = sp.user_playlist_create(usr, name, public=False, collaborative=False, description=description)
         while res['name'] not in [p['name'] for p in self.playlists]:
               self.playlists = self.retrieve(PLAYLIST)
               sleep(2)        
         return res
   
   def get_track_ids(self, p):
      try:
         return [t['track']['id'] for t in self.retrieve(TRACK, pid=p['id'])]
      except:
         lst = []
         for t in self.retrieve(TRACK, pid=p['id']):
            try: #!
               lst.append(t['track']['id'])
            except:
               try:
                  print(t['track']['name'])
               except:
                  pass
         return lst

   def prcs(self, a, b):
      if a == SAVED:
         a = self.sids
      elif type(a) == str: #! assume id..or NAME
         a = self.get_track_ids(self.pname(a))
      elif type(a) == dict: #! assume id..or NAME
         a = self.get_track_ids(a)

      if b == SAVED:
         b = self.sids
      elif type(b) == str: #! assume id..or NAME
         b = self.get_track_ids(self.pname(b))
      elif type(b) == dict: #! assume id..or NAME
         b = self.get_track_ids(b)
      #lse list of track_ids
      return a, b
   def diff(self, a, b):
      a, b = self.prcs(a,b)
      return list(set(a) - set(b))
   def intersect(self, a, b):
      a, b = self.prcs(a,b)
      return list(set(a).intersection(set(b)))
