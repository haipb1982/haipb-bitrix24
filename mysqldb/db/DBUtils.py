import pymysql
from dbutils.steady_db import connect

from utils import log
# LOGGER = log.get_logger(__name__)

from utils.Logger import Logger
LOGGER = Logger(__name__).get()

config = {
    'host': 'host.docker.internal',
    'port':'3306',
    'user': 'vnztech',
    'password': 'Vietnam@68',
    'database': 'vnztech_blubx24'
}

class DBUtils:

  __connection = None;
  __cursor = None;

  def __init__(self):
        __db_config = config['mysql'];
        self.__connection = pymysql.connect(host=__db_config['host'],
                                            user = __db_config['user'],
                                            password = __db_config['password'],
                                            db = __db_config['db'],
                                            autocommit = True, charset = 'utf8mb4', 
                                            cursorclass = pymysql.cursors.DictCursor)
        self.__cursor = self.__connection.cursor();

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
          LOGGER.error('mySQL ERROR:',{"extra":err})
          LOGGER.error('mySQL ERROR query:' ,extra={"extra":query})
          LOGGER.error('mySQL ERROR params:' ,extra={"extra":params})
          result['status'] = False
          result['code'] = 500
          result['message'] = f'error:{err}'
          result['data'] = None
          # self.__connection.rollback()
    #   finally:
    #       self.close()
      return result

  def close(self):
      self.__connection.close()
      self.__cursor.close()