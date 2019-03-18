import psycopg2
import json
import sys
from datetime import datetime as dt

i = 10

def analysis(webpage_id, k = 2, db = 'zumamotu', user = 'MaximZubkov', password='maxTBMzu', host='localhost', port='1234'):
	SELECT_RECENT_k_RECORDS = ''' SELECT * FROM data
								  WHERE webpage_id = {}
								  ORDER BY ts 
								  DESC LIMIT {}'''.format(webpage_id, k)
	with psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port) as conn:
		with conn.cursor() as cursor:
			cursor.execute(SELECT_RECENT_k_RECORDS)
			tmp = cursor.fetchall()
			print(tmp)
			if tmp:
				print(webpage_id, " ", k)
				model = "h"
				UPDATE_MODEL = '''UPDATE webpage SET model = '{}'
								  WHERE id = {};'''.format(str(model), webpage_id)
				cursor.execute(UPDATE_MODEL)
				conn.commit()
			else:
				retrun -1


if __name__ == "__main__":
	if len(sys.argv) == 3:
		webpage_id = sys.argv[1]
		k = sys.argv[2]
		analysis(webpage_id, k)
	if len(sys.argv) == 8:
		webpage_id = sys.argv[1]
		k = sys.argv[2]
		db = sys.argv[3]
		user = sys.argv[4]
		password = sys.argv[5]
		host = sys.argv[6]
		port = sys.argv[7]
		analysis(webpage_id, k, db, user, password, host, port)
