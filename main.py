from ___sam import *
import re
from concurrent.futures import ThreadPoolExecutor
e = ThreadPoolExecutor(max_workers=5)
jprint = lambda x: print(json.dumps(x,indent=2))

mem = SAM(sp)


def reset():
   """
   Move everything into cache and save json file
   """

   return


if __name__ == '__main__':
   
   # pnew = mem.pname('New')

   fn = 'heard.json'
   bk = {}
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
   count = 0
   for p in owned:
      # print(p['name'])
      # if('Cache' in p['name']):
      #    continue
      track_ids = mem.get_track_ids(p)
      # bk[p['id']] = {
      #    "id":p['id'],
      #    "name":p['name'],
      #    "description":p['description'],
      #    "tracks": track_ids
      # }
      lst.update(track_ids)
      # while(len(mem.get_track_ids(mem.pname(f'Cache {count}'))) > 2000):
      #    count += 1
      #    print(count)
      # mem.move(None, mem.pname(f'Cache {count}')['id'], track_ids)
      # sp.current_user_unfollow_playlist(p['id'])
      # with open('data/backup.json', 'w') as f:
      #    json.dump(bk, f, indent=2)
   # bk['saved'] = {
   #    "id":'saved',
   #    "name":"Liked Songs",
   #    "tracks": mem.sids
   # }
   lst.update(mem.sids)
   # mem.move(None, mem.pname(f'Cache {count}')['id'], mem.sids)
   # with open('data/backup.json', 'w') as f:
   #    json.dump(bk, f, indent=2)

   red = mem.pname('reduce')
   radio_mixes = [p for p in mem.playlists if 'Mix' in p['name'] or 'Radio' in p['name']]
   unowned = [p for p in mem.playlists if p['owner']['id'] != usr]
   def fnctn(p):
      global lst
      # pn = re.sub('(Mix|Radio)', '', p['name'])
      # pn = re.sub('Radio', '', p['name'])
      # ref = mem.pname(f'{p} Mix')
      # ref2 = mem.pname(f'{pn} New', description='.new')
      new_tracks = mem.diff(mem.get_track_ids(p), lst)
      print(p['name'], len(new_tracks))
      mem.move( None, red['id'], new_tracks)

      lst.update(new_tracks)
   futures = []
   for p in unowned:
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
      futures.append(e.submit(fnctn, p))
   for f in futures:
      f.result()
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


      #NEXT remove tracks from music (owned)