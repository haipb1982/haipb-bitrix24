import os
import sqlite3

from dao import db


def add_new_product(hanravan_id, bitrix24_id, note):
    sql = '''INSERT INTO tbl_product(haravan_id, bitrix24_id, note) VALUES (?,?,?)'''
    pamrs = [hanravan_id, bitrix24_id, note]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return True
    else:
        print(res.get("data"))
        return False


def get_by_haravan_id(id):
    sql = '''SELECT * FROM tbl_product WHERE haravan_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    if res.get("status"):
        return res.get("data")
    return None


def get_by_bitrix24_id(id):
    sql = '''SELECT * FROM tbl_product WHERE bitrix24_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    return res

def delete_by_haravan_id(id):
    sql = '''DELETE FROM tbl_product WHERE haravan_id = ?'''
    pamrs = [id]
    res = db.fetchSQL(sql, pamrs)
    return res