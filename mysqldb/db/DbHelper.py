import pymysql.cursors
import pymysql
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

    def query(self, query, params):
        result = {}
        try:
            self.__cursor.execute(query, params)            
            result['status'] = True
            result['code'] = 200
            result['message'] = 'success'
            result['data'] = self.__cursor.fetchall()
            self.__connection.commit()
        except Exception as err:
            print('\033[91m','mySQL ERROR:',err, '\033[0m')
            print('\033[92m','mySQL ERROR query:',query, '\033[0m')
            print('mySQL ERROR params:', params)
            result['status'] = False
            result['code'] = 500
            result['message'] = f'error:{err}'
            result['data'] = None
            # self.__connection.rollback()
        # finally:
            # self.__connection.close()
        return result

    def close(self):
        self.__connection.close();