from mysqldb.db.DbHelper import DbHelper


class RetryJobDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    # # # for webapp API # # #
    def getAllRetryJobRecords(self,retry_time_limit=5):
        res = self.__db.fetch("SELECT id,haravan_id,bitrix24_id, haravan_data, type, action, retry_times FROM tbl_retry_job WHERE retry_times < %s ORDER BY id DESC", (retry_time_limit))
        
        return res

    def deleteRetryJobRecord(self,id):
        res = self.__db.execute("DELETE FROM tbl_retry_job WHERE id=%s", id)
        
        return res
    
    def insertRetryJobRecord(self, haravan_id, bitrix24_id, haravan_data="", bitrix_data="", type="", action=""):
        sql = '''INSERT INTO tbl_retry_job (haravan_id, bitrix24_id, haravan_data, bitrix_data, type, action) VALUES (%s,%s,%s,%s,%s,%s)'''        
        pamrs =  [haravan_id, bitrix24_id, haravan_data, bitrix_data, type, action]
        res = self.__db.execute(sql,pamrs)
        
        return res
    
    def updateRetryTime(self):
        res = self.__db.execute("UPDATE tbl_retry_job SET retry_times=retry_times + 1", None)
        
        return res
    