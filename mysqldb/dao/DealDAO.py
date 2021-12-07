from mysqldb.db.DbHelper import DbHelper


class DealDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    def getAllDeals(self):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,havavan_status,bitrix_status,update_ts FROM tbl_deal_order", None)
        return res.get('data')

    def getAllDealsPages(self, __from, __to):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,havavan_status,bitrix_status,update_ts FROM tbl_deal_order LIMIT %s,%s", (__from, __to))
        return res.get('data')
    
    def deleteDealRecord(self,id):
        res = self.__db.query("DELETE FROM tbl_deal_order WHERE id=%s", id)
        return res.get('data')
    
    def updateDealRecord(self,id, haravan_id, bitrix24_id):
        res = self.__db.query("UPDATE tbl_deal_order SET haravan_id=%s, bitrix24_id=%s WHERE id=%s", (haravan_id,bitrix24_id,id))
        return res.get('data')
    
    def insertDealRecord(self, hanravan_id, bitrix24_id):
        # print('addNewDeal',hanravan_id,bitrix24_id)
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id) VALUES (%s,%s)'''
        pamrs = [hanravan_id, bitrix24_id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            print('--> insertDealRecord successful ',hanravan_id,bitrix24_id)
            return True
        else:
            print('--> insertDealRecord failed ',hanravan_id,bitrix24_id)
            print(res.get("data"))
            return False

    def addNewDeal(self, hanravan_id, bitrix24_id, haravan_data="", bitrix_data=""):
        # print('addNewDeal',hanravan_id,bitrix24_id)
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (%s,%s,%s,%s)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            print('--> addNewDeal successful ',hanravan_id,bitrix24_id)
            return True
        else:
            print('--> addNewDeal failed ',hanravan_id,bitrix24_id)
            print(res.get("data"))
            return False

    def updateDeal(self, id, haravan_data="", bitrix_data=""):
        # print('updateDeal',id)
        sql = '''UPDATE tbl_deal_order SET haravan_data=%s, bitrix_data=%s WHERE haravan_id=%s'''
        pamrs = [haravan_data, bitrix_data, id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            print('--> updateDeal successful ',id)
            return True
        else:
            print('--> updateDeal failed ',id)
            print(res.get("data"))
            return False

    def getHaravanID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = %s'''
        pamrs = [id]
        res = self.__db.query(sql, pamrs)
        if res.get("status"):
            return res.get("data")
        return None

    def getDataByHaID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = %s'''
        pamrs = [id]
        res = self.__db.query(sql, pamrs)
        if res.get("status"):
            return res.get("data")
        return None
    
    def getDataByBxID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = %s'''
        pamrs = [id]
        res = self.__db.query(sql, pamrs)
        if res.get("status"):
            return res.get("data")
        return None

    def getBitrix24ID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = %s'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_haravan_id(self, id):
        sql = '''UPDATE tbl_deal_order SET haravan_status = %s WHERE haravan_id = %s'''
        pamrs = ["DELETE", id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self, id):
        sql = '''UPDATE tbl_deal_order SET bitrix_status = %s WHERE bitrix24_id = %s'''
        pamrs = ["DELETE", id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return res.get("data")
        return None
