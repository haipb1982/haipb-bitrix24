import os
import pathlib
import sqlite3


def addNewDeal(hanravan_id, bitrix24_id, note):
    sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id, note) VALUES (?,?,?)'''
    pamrs = [hanravan_id, bitrix24_id, note]
    res = fetchSQL(sql, pamrs)
    if res.get("status"):
        return True
    else:
        print(res.get("data"))
        return False


def getHaravanID(id):
    sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = ?'''
    pamrs = [id]
    res = fetchSQL(sql, pamrs)
    if res.get("status"):
        return res.get("data")
    return None


def getBitrix24ID(id):
    sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = ?'''
    pamrs = [id]
    res = fetchSQL(sql, pamrs)
    return res


def initDB():
    pamrs = []
    # Create table
    sql = '''CREATE TABLE tbl_deal_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            haravan_id INTEGER NOT NULL UNIQUE,
            bitrix24_id INTEGER NOT NULL UNIQUE,
            note text )'''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])

    sql = '''
        SELECT * FROM tbl_deal_order
        '''
    res = fetchSQL(sql, pamrs)
    if res['status']:
        print(res['data'])


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


# main for testing
if __name__ == "__main__":

    initDB()

    res = addNewDeal(1236954857, 3259, 'test migrate')
    print(res['data'])

    res = getHaravanID(1236954857)
    print(res['data'])

    res = getBitrix24ID(3259)
    print(res['data'])

    pass
