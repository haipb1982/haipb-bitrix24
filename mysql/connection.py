import mysql.connector
from mysql.connector import errorcode

# Cpanel - phpmyAdmin
# url: http://45.252.249.23:2083/
# user: asuofvsy
# pwd: vpin.pinart123

config = {
  'host': '45.252.249.23',
  'user': 'asuofvsy_haipb',
  'password': '@Vietnam68',
  'database': 'asuofvsy_blu',
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