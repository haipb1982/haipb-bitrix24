from mysqldb.db.DbHelper import DbHelper


class ContactDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    def getAllContacts(self):
        return self.__db.query("SELECT * FROM tbl_contact_customer", None).fetchall()

    def add_new_contact(self,hanravan_id, bitrix24_id, haravan_data, bitrix_data):
        sql = '''INSERT INTO tbl_contact_customer(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (?,?,?,?)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data ]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False


    def get_by_haravan_id(self,id):
        sql = '''SELECT * FROM tbl_contact_customer WHERE haravan_id = ?'''
        pamrs = [id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None


    def get_by_bitrix24_id(self,id):
        sql = '''SELECT * FROM tbl_contact_customer WHERE bitrix24_id = ?'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self, id):
        sql = '''UPDATE tbl_contact_customer SET bitrix_status = ? WHERE bitrix24_id = ?'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def update_by_haravan_id(self,id, haravan_data="", bitrix_data=""):
        sql = '''UPDATE tbl_contact_customer SET haravan_data=?, bitrix_data=? WHERE haravan_id=?'''
        pamrs = [haravan_data, bitrix_data, id]
        
        res = self.__db.query(sql, pamrs).fetchall()
        
        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def delete_by_haravan_id(self,id):
        sql = '''UPDATE tbl_contact_customer SET haravan_status = ? WHERE haravan_id = ?'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None