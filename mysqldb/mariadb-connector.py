 # Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="blu_bitrix24",
        password="6(aLWwks[(qnS)3*",
        host="103.159.51.249",
        port=3306,
        database="blu_bitrix24"

    )
    print('Connect successful!')
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()