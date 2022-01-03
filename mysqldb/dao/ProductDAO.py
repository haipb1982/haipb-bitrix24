from mysqldb.db.DbHelper import DbHelper


class ProductDAO(object):
    __db = None

    def __init__(self):
        self.__db = DbHelper()

    # # # for webapp API # # #
    def getAllProducts(self):
        res = self.__db.query("SELECT id,haravan_id,haravan_data,bitrix24_id,bitrix_status,update_ts,haravan_status FROM tbl_product ORDER BY id DESC", None)
        self.__db.close()
        return res
        

    def getAllProductsPages(self, __from, __to):
        res = self.__db.query("SELECT id,haravan_id,haravan_data,bitrix24_id,bitrix_status,update_ts,haravan_status FROM tbl_product LIMIT %s,%s ORDER BY id DESC", (__from, __to))
        self.__db.close()
        return res
    
    def deleteProductRecord(self,id):
        res = self.__db.query("DELETE FROM tbl_deal_order WHERE id=%s", id)
        self.__db.close()
        return res
    
    def updateProductRecord(self,id, haravan_id, bitrix24_id):
        res = self.__db.query("UPDATE tbl_deal_order SET haravan_id=%s, bitrix24_id=%s WHERE id=%s", (haravan_id,bitrix24_id,id))
        self.__db.close()
        return res
    
    def insertProductRecord(self, hanravan_id, bitrix24_id):
        sql = '''INSERT INTO tbl_deal_order(haravan_id, bitrix24_id) VALUES (%s,%s)'''
        res = self.__db.query(sql, (hanravan_id, bitrix24_id))
        self.__db.close()
        return res
    
    # # # # # # # 
    
    def add_new_product(self,hanravan_id, bitrix24_id, haravan_data, bitrix_data):
        sql = '''INSERT INTO tbl_product(haravan_id, bitrix24_id, haravan_data, bitrix_data) VALUES (%s,%s,%s,%s)'''
        pamrs = [hanravan_id, bitrix24_id, haravan_data, bitrix_data]
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False


    def get_by_haravan_id(self,id):
        sql = '''SELECT * FROM tbl_product WHERE haravan_id = %s'''
        pamrs = [id]

        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status"):
            data = res.get("data")
            if len(data) > 0 :
                return data[0]
        return None


    def get_by_bitrix24_id(self,id):
        sql = '''SELECT * FROM tbl_product WHERE bitrix24_id = %s'''
        pamrs = [id]
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status"):
            data = res.get("data")
            if len(data) > 0 :
                return data[0]
        return None

    def update_by_haravan_id(self,id, haravan_data="", bitrix_data=""):
        sql = '''UPDATE tbl_product SET haravan_data=%s, bitrix_data=%s WHERE haravan_id=%s'''
        pamrs = [haravan_data, bitrix_data, id]
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()

        if res.get("status"):
            return True
        else:
            print(res.get("data"))
            return False

    def delete_by_haravan_id(self,id):
        sql = '''UPDATE tbl_product SET haravan_status = %s WHERE haravan_id = %s'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status"):
            return res.get("data")
        return None

    def delete_by_bitrix_id(self,id):
        sql = '''UPDATE tbl_product SET bitrix_status = %s WHERE bitrix24_id = %s'''
        pamrs = ["DELETE", id]
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status"):
            return res.get("data")
        return None

    def get_product_limit_1(self):
        sql = '''SELECT * FROM tbl_product WHERE bitrix_status != 'DELETE' and haravan_status != 'DELETE' limit 1 '''
        pamrs = []

        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status") and len(res.get("data")) > 0:
            return res.get("data")[0]
        return None

    def get_products(self):
        sql = '''SELECT * FROM tbl_product'''
        pamrs = []
        
        res = self.__db.query(sql, pamrs)
        self.__db.close()
        
        if res.get("status") and len(res.get("data")) > 0:
            data = res.get("data")
            return list(data)
        return []
