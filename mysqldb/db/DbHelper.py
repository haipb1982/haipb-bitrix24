import pymysql.cursors
import pymysql
import json
from mysqldb.config import config


class DbHelper:

    __connection = None;
    __cursor = None;

    def __init__(self):
        __db_config = config['mysql'];
        self.__connection = pymysql.connect(host=__db_config['host'],
                                            user = __db_config['user'],
                                            password = __db_config['password'],
                                            db = __db_config['db'],
                                            charset = 'utf8mb4',
                                            cursorclass = pymysql.cursors.DictCursor);
        self.__cursor = self.__connection.cursor();
    
    # def query(self, query, params):
    #    self.__cursor.execute(query, params)
    #    return self.__cursor;
    def default(self,obj):
        """Default JSON serializer."""
        import calendar, datetime

        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            millis = int(
                calendar.timegm(obj.timetuple()) * 1000 +
                obj.microsecond / 1000
            )
            return millis
        raise TypeError('Not sure how to serialize %s' % (obj,))

    def dbresponse(self,status=True,code=200,message='success',data=None):
        res = {}
        res['status'] = status
        res['code'] = code
        res['message'] = message
        # res['data'] = json.dumps(data, default=self.default)
        res['data'] = data
        return res

    def query(self, query, params):
        result = {}
        try:
            self.__cursor.execute(query, params)            
            result = self.dbresponse(data=self.__cursor.fetchall())
            self.__connection.commit()
        except Exception as err:
            print('\033[91m','mySQL ERROR:',err, '\033[0m')
            print('\033[92m','mySQL ERROR query:',query, '\033[0m')
            print('mySQL ERROR params:', params)
            result = self.dbresponse(False,500,f'error:{err}',None)
            # self.__connection.rollback()
        # finally:
            # self.__connection.close()
        return result

    def execute(self, query, params):
        result = {}
        try:
            self.__cursor.execute(query, params)            
            result = self.dbresponse(data=self.__cursor.fetchall())
            self.__connection.commit()
        except Exception as err:
            print('\033[91m','mySQL ERROR:',err, '\033[0m')
            print('\033[92m','mySQL ERROR query:',query, '\033[0m')
            print('mySQL ERROR params:', params)
            result = self.dbresponse(False,500,f'error:{err}',None)
            # self.__connection.rollback()
        # finally:
            # self.__connection.close()
        return result

    def fetch(self, query, params):
        result = {}
        try:
            self.__cursor.execute(query, params)            
            data = self.__cursor.fetchall()
            # print(data)
            result = self.dbresponse(data=data)
        except Exception as err:
            print('\033[91m','mySQL ERROR:',err, '\033[0m')
            print('\033[92m','mySQL ERROR query:',query, '\033[0m')
            print('mySQL ERROR params:', params)
            result = self.dbresponse(False,500,f'error:{err}',None)
            # self.__connection.rollback()
        # finally:
            # self.__connection.close()
        return result

    def close(self):
        self.__connection.close();

    

