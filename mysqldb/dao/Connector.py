import mysql.connector
from mysql.connector import errorcode
from mysql.connector import connect, Error

# 'host':'103.159.51.249'
# "host":"host.docker.internal",
config = {
  'host': '103.159.51.249',
  'user': 'vnztech',
  'password': 'Vietnam@68',
  'database': 'vnztech_blubx24',
  'raise_on_warnings': True
}

def query(sql,parm):
  try:
    with connect(**config) as connection:
        with connection.cursor() as cursor:
            for result in cursor.execute(sql, parm, multi=True):
                if result.with_rows:
                    print(result.fetchall())
            connection.commit()
  except Error as e:
      print(e)

  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  connection.close()

