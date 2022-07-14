from ___sam import *
import re, os
import pydash as _
from concurrent.futures import ThreadPoolExecutor
jprint = lambda x: print(json.dumps(x,indent=2))

mem = SAM(sp)
last = 'nope'
e = ThreadPoolExecutor(max_workers=5)
p = mem.pname('reduce')
lst = mem.get_track_ids(p)
seek = True
# lk = {}
count = 0
mem.move(p['id'], None, mem.sids)
while 1:
   res = sp.currently_playing()
   prog = res['progress_ms']
   t = res['item']
   sid = t['id']
   if seek and not count%3:
      sp.seek_track(prog + 20000)
   count += 1
   print(count)
   # try:
   #    if count == 15:
   #       sp.next_track()
   # except spotipy.exceptions.SpotifyException:
   #    pass
   if last != sid:
      count = 0
      future = e.submit(sp.artists, [a['id'] for a in t['artists']])
      os.system('clear')
      
      if last in lst:
         mem.move(p['id'], None, [last])
         # print('Removed')
      artists = future.result()['artists']
      print(', '.join([a['name'] for a in artists]), ' - ', t['name'])
      genres = list(set(_.flatten([a['genres'] for a in artists])))
      print(genres)
      last = sid
   sleep(2)

def try_this():
   # sp.recommendation
   return