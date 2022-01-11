from mysqldb.db.DbHelper import DbHelper
from mysqldb.db.DBUtils import DBUtils


class DealDAO(object):
    __db = None

    def __init__(self):
        # self.__db = DbHelper()
        self.__db = DBUtils()


    # # # for webapp API # # #
    def getAllDeals(self):
        res = self.__db.query("SELECT id, name, haravan_id,bitrix24_id,havavan_status, bitrix_status,update_ts FROM tbl_deal_order ORDER BY id DESC", None)
        return res

    def getDealOrderByHaID(self,haravan_id):
        res = self.__db.query("SELECT id,name, haravan_id,bitrix24_id,havavan_status, bitrix_status,update_ts FROM tbl_deal_order WHERE haravan_id=%s", (haravan_id,))
        return res

    def getDealOrderByIDs(self,haravan_id='',bitrix24_id=''):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,havavan_status, haravan_data, bitrix_status,update_ts FROM tbl_deal_order WHERE haravan_id=%s or bitrix24_id=%s", (haravan_id,bitrix24_id))
        return res

    def getAllDealsPages(self, __from, __to):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,havavan_status,haravan_data,bitrix_status,update_ts FROM tbl_deal_order LIMIT %s,%s ORDER BY id DESC", (__from, __to))
        return res
    
    def getMaxDealID(self):
        res = self.__db.query("SELECT MAX(bitrix24_id) as bitrix24_id FROM tbl_deal_order", None)
        return res
    
    def deleteDealRecord(self,id):
        res = self.__db.query("DELETE FROM tbl_deal_order WHERE id=%s", id)
        return res
    
    def updateDealRecord(self,id, haravan_id, bitrix24_id):
        res = self.__db.query("UPDATE tbl_deal_order SET haravan_id=%s, bitrix24_id=%s WHERE id=%s", (haravan_id,bitrix24_id,id))
        return res
    
    def updateNameRecord(self,name='BLU ORDER DEAL NAME',id='', haravan_id='',bitrix24_id=''):
        sql = "UPDATE tbl_deal_order SET name=%s WHERE haravan_id=%s OR bitrix24_id=%s OR id=%s"
        parms = (name,haravan_id,bitrix24_id,id)
        res = self.__db.query(sql, parms)
        
        return res

    def insertDealRecord(self, haravan_id, bitrix24_id):
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id) VALUES (%s,%s)'''        
        res = self.__db.query(sql, (haravan_id, bitrix24_id))
        return res
    
    # # # # # #

    def addNewDeal(self, hanravan_id, bitrix24_id, haravan_data="", bitrix_data=""):
        # print('addNewDeal',hanravan_id,bitrix24_id)
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (%s,%s,%s,%s)'''
        parms = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]

        res = self.__db.query(sql, parms)

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
        parms = [haravan_data, bitrix_data, id]

        res = self.__db.query(sql, parms)

        if res.get("status"):
            print('--> DAO updateDeal successful ',id)
            return True
        else:
            print('--> DAO updateDeal failed ',id)
            print(res.get("data"))
            return False

    def getHaravanID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = %s'''
        parms = [id]
        res = self.__db.query(sql, parms)
        if res.get("status"):
            return res.get("data")
        return None

    def getDataByHaID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE haravan_id = %s'''
        parms = [id]
        res = self.__db.query(sql, parms)
        if res.get("status"):
            return res.get("data")
        return None
    
    def getDataByBxID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = %s'''
        parms = [id]
        res = self.__db.query(sql, parms)
        if res.get("status"):
            return res.get("data")
        return None

    def getBitrix24ID(self, id):
        sql = '''SELECT * FROM tbl_deal_order WHERE bitrix24_id = %s'''
        parms = [id]

        res = self.__db.query(sql, parms)

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_haravan_id(self, id):
        sql = '''UPDATE tbl_deal_order SET haravan_status = %s WHERE haravan_id = %s'''
        parms = ["DELETE", id]

        res = self.__db.query(sql, parms)

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self, id):
        sql = '''UPDATE tbl_deal_order SET bitrix_status = %s WHERE bitrix24_id = %s'''
        parms = ["DELETE", id]

        res = self.__db.query(sql, parms)

        if res.get("status"):
            return res.get("data")
        return None
