import pymysql
from dbutils.steady_db import connect
import time

dbconfig = {
    'host': '103.159.51.249',
    'port':'3306',
    'user': 'vnztech',
    'password': 'Vietnam@68',
    'database': 'vnztech_blubx24'
}

db = connect(
  creator = pymysql, # the rest keyword arguments belong to pymysql
  host=dbconfig['host'], user=dbconfig["user"],
                 password=dbconfig["password"], database=dbconfig["database"],
  autocommit = True, charset = 'utf8mb4', 
  cursorclass = pymysql.cursors.DictCursor)

 # test...
while True:
    t0 = time.time()
    for i in range(10):
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM tbl_deal_order')
        res = cur.fetchone()
        print(res)
        cur.close()  # or del cur
        db.close()  # or del db
    print("time cousumed:", time.time() - t0)
