import os
import sqlite3


def fetchSQL(sql, pamrs):
    result = {}
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    strdir = os.path.join(DIR_PATH, "", 'blusaigon.db')
    con = sqlite3.connect(strdir)
    cur = con.cursor()
    try:
        cur.execute(sql, pamrs)
        result['status'] = True
        result['data'] = cur.fetchone()
        con.commit()
    except sqlite3.Error as err:
        result['status'] = False
        result['data'] = err
    con.close()
    return result

def _init_deal():
    pamrs = []
    # Create table
    sql = '''CREATE TABLE tbl_deal_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            haravan_id INTEGER NOT NULL UNIQUE,
            bitrix24_id INTEGER NOT NULL UNIQUE,
            haravan_data text,
             bitrix_data text,
             status VARCHAR(365)
             )'''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

    sql = '''
        SELECT * FROM tbl_deal_order
        '''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])


def _init_product():
    pamrs = []
    # Create table
    sql = '''CREATE TABLE tbl_product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            haravan_id INTEGER NOT NULL UNIQUE,
            bitrix24_id INTEGER NOT NULL UNIQUE,
            haravan_data text,
             bitrix_data text,
             status VARCHAR(365)
            )'''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

    sql = '''
        SELECT * FROM tbl_product
        '''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

def _init_customer():
    pamrs = []
    # Create table
    sql = '''CREATE TABLE tbl_contact_customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            haravan_id INTEGER NOT NULL UNIQUE,
            bitrix24_id INTEGER NOT NULL UNIQUE,
            haravan_data text,
             bitrix_data text,
             status VARCHAR(365)
             )'''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

    sql = '''
        SELECT * FROM tbl_contact_customer
        '''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

def init_db():
    _init_deal()
    _init_product()
    _init_customer()