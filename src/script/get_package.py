import redis
import pickle
DATA_HOST='127.0.0.1'
DATA_DBID=1
red = redis.StrictRedis(host=DATA_HOST, port='6379', db=DATA_DBID)
i = 0
for r in red.keys("package:*"):
	package, zone, uid, vid = r.split(':')
	print package, zone, uid, vid
	i+=1
print i
#zone_list = [1, 2, 3, 100, 101, 200, 201, 300]

		#red.hset('hp:%s' % one, x, int(str(y)[:-4]+ str(y)[-4:].zfill(5)))
	

