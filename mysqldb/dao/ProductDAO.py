from mysqldb.db.DbHelper import DbHelper


class ProductDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    def getAllProducts(self):
        return self.__db.query("SELECT * FROM tbl_product", None).fetchall()
    
    def add_new_product(self,hanravan_id, bitrix24_id, haravan_data, bitrix_data):
        sql = '''INSERT INTO tbl_product(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (?,?,?,?)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False


    def get_by_haravan_id(self,id):
        sql = '''SELECT * FROM tbl_product WHERE haravan_id = ?'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs).fetchall()
        
        if res.get("status"):
            return res.get("data")
        return None


    def get_by_bitrix24_id(self,id):
        sql = '''SELECT * FROM tbl_product WHERE bitrix24_id = ?'''
        pamrs = [id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def update_by_haravan_id(self,id, haravan_data="", bitrix_data=""):
        sql = '''UPDATE tbl_product SET haravan_data=?, bitrix_data=? WHERE haravan_id=?'''
        pamrs = [haravan_data, bitrix_data, id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def delete_by_haravan_id(self,id):
        sql = '''UPDATE tbl_product SET haravan_status = ? WHERE haravan_id = ?'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self,id):
        sql = '''UPDATE tbl_product SET bitrix_status = ? WHERE bitrix24_id = ?'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status"):
            return res.get("data")
        return None

    def get_product_limit_1(self):
        sql = '''SELECT * FROM tbl_product WHERE bitrix_status != 'DELETE' and haravan_status != 'DELETE' limit 1 '''
        pamrs = []

        res = self.__db.query(sql, pamrs).fetchall()
        
        if res.get("status") and len(res.get("data")) > 0:
            return res.get("data")[0]
        return None

    def get_products(self):
        sql = '''SELECT * FROM tbl_product'''
        pamrs = []
        
        res = self.__db.query(sql, pamrs).fetchall()

        if res.get("status") and len(res.get("data")) > 0:
            data = res.get("data")
            return list(data)
        return []
