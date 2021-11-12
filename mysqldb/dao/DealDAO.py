from mysqldb.db.DbHelper import DbHelper


class DealDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    def getAllDeals(self):
        return self.__db.query("SELECT * FROM tbl_deal_order", None).fetchall()

    def addNewDeal(self, hanravan_id, bitrix24_id, haravan_data="", bitrix_data=""):
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (?,?,?,?)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def updateDeal(self, id, haravan_data="", bitrix_data=""):

        sql = '''UPDATE tbl_deal_order SET haravan_data=?, bitrix_data=? WHERE haravan_id=?'''
        pamrs = [haravan_data, bitrix_data, id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def getHaravanID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = ?'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def getBitrix24ID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = ?'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_haravan_id(self, id):
        sql = '''UPDATE tbl_deal_order SET haravan_status = ? WHERE haravan_id = ?'''
        pamrs = ["DELETE", id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self, id):
        sql = '''UPDATE tbl_deal_order SET bitrix_status = ? WHERE bitrix24_id = ?'''
        pamrs = ["DELETE", id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None
