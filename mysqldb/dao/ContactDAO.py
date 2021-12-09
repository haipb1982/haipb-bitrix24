from mysqldb.db.DbHelper import DbHelper


class ContactDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    
    def getAllContacts(self):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,bitrix_status,update_ts,haravan_status FROM tbl_contact_customer", None)
        if res.get("status"):
            return res
        else:
            return None

    def getAllContactsPages(self, __from, __to):
        res = self.__db.query("SELECT id,haravan_id,bitrix24_id,bitrix_status,update_ts,haravan_status FROM tbl_contact_customer LIMIT %s,%s", (__from, __to))
        return res

    def get_contacts(self):
        res = self.__db.query("SELECT * FROM tbl_contact_customer", None)
        if res.get("status"):
            return res.get("data")
        else:
            return None

    def add_new_contact(self,hanravan_id, bitrix24_id, haravan_data, bitrix_data):
        sql = '''INSERT INTO tbl_contact_customer(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (%s,%s,%s,%s)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data ]
        
        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False


    def get_by_haravan_id(self,id):
        sql = '''SELECT * FROM tbl_contact_customer WHERE haravan_id = %s'''
        pamrs = [id]
        
        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            data = res.get("data")
            if len(data) > 0 :
                return data[0]
        return None


    def get_by_bitrix24_id(self,id):
        sql = '''SELECT * FROM tbl_contact_customer WHERE bitrix24_id = %s'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            data = res.get("data")
            if len(data) > 0 :
                return data[0]
        return None

    def delete_by_bitrix_id(self, id):
        sql = '''UPDATE tbl_contact_customer SET bitrix_status = %s WHERE bitrix24_id = %s'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return res.get("data")
        return None

    def update_by_haravan_id(self,id, haravan_data="", bitrix_data=""):
        sql = '''UPDATE tbl_contact_customer SET haravan_data=%s, bitrix_data=%s WHERE haravan_id=%s'''
        pamrs = [haravan_data, bitrix_data, id]
        
        res = self.__db.query(sql, pamrs)
        
        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def delete_by_haravan_id(self,id):
        sql = '''UPDATE tbl_contact_customer SET haravan_status = %s WHERE haravan_id = %s'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs)

        if res.get("status"):
            return res.get("data")
        return None