import mysql.connector
from mysql.connector import errorcode

# "host":"host.docker.internal",
config = {
  'host': '103.159.51.249',
  'user': 'vnztech',
  'password': 'Vietnam@68',
  'database': 'vnztech_blubx24',
  'raise_on_warnings': True
}

try:
  cnx = mysql.connector.connect(**config)
  print("Connection is successful!")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()