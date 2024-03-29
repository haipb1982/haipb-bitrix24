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


def updateDeal(id, haravan_data="", bitrix_data=""):
    sql = '''UPDATE tbl_deal_order SET haravan_data=?, bitrix_data=? WHERE haravan_id=?'''
    pamrs = [haravan_data, bitrix_data, id]
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
    if res.get("status"):
        return res.get("data")
    return None

def delete_by_haravan_id(id):
    sql = '''UPDATE tbl_deal_order SET haravan_status = ? WHERE haravan_id = ?'''
    pamrs = ["DELETE", id]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return res.get("data")
    return None

def delete_by_bitrix_id(id):
    sql = '''UPDATE tbl_deal_order SET bitrix_status = ? WHERE bitrix24_id = ?'''
    pamrs = ["DELETE", id]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return res.get("data")
    return None



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
