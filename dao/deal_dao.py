import os
import pathlib
import sqlite3

from dao import db


def addNewDeal(hanravan_id, bitrix24_id, haravan_data="", bitrix_data=""):
    sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (?,?,?,?)'''
    pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return True
    else:
        print(res.get("data"))
        return False


def getHaravanID(id):
    sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return res.get("data")
    return None


def getBitrix24ID(id):
    sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    return res

def deleteHaravanID(id):
    sql = '''DELETE FROM tbl_deal_order WHERE haravan_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    return res



# main for testing
if __name__ == "__main__":
    db._init_deal()

    res = addNewDeal(1236954857, 3259, 'test migrate')
    print(res['data'])

    res = getHaravanID(1236954857)
    print(res['data'])

    res = getBitrix24ID(3259)
    print(res['data'])

    pass
