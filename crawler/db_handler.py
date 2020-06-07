#coding: utf-8
from DBUtils.PooledDB import PooledDB
import pymysql
from crawler.config import host,port,username,password,database,charset,table_name
from crawler.my_logger import logger


POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建

    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，
    #因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，
    #_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never,
    # 1 = default = whenever it is requested, 2 = when a cursor
    #is created, 4 = when a query is executed, 7 = always
    host=host,
    port=port,
    user=username,
    password=password,
    database=database,
    charset=charset
)


class DB():
    def __init__(self):
        self.connect = POOL.connection()
        self.db = self.connect.cursor()
        self.db.execute('use  %s;' %database)

    def create_table(self, create_sql):
        '''

        :param create_sql:创建表的SQL语句
        :return: 成功返回1，数据表已存在返回0， 失败返回-1
        '''
        try:
            self.db.execute(create_sql)
            return 1
        except Exception as e:
            if e == 'Table' + create_sql + 'already exists':
                return 0
            else:
                return -1

    def commit(self):
        self.connect.commit()


    def insert_data(self, data, table_name=table_name):
        '''
        :param data: 一个字典
        :param table_name: 表名
        :return: 成功返回1，失败返回0
        '''
        columns = ()
        vals = ()
        for key in data:
            if data[key]:
                columns += (key,)
                vals += (data[key],)
        sql = "INSERT INTO " + table_name + str(columns).replace('\'','') +" VALUES" + str(vals)
        try:
            self.db.execute(sql)
            self.commit()
            print(sql)
            return 1
        except Exception as e:/home/huawenjin
            if 'Duplicate' in str(e):
                return 1
            logger.info(e)
            return 0

    def insert_one(self,data, table_name):
        '''

        :param data: 一个元祖(column,val)
        :param table_name: 表名
        :return:  成功返回1，失败返回0
        '''
        column = data[0]
        val = data[1]
        sql = "INSERT INTO " + table_name +" (%s) values('%s')" %(column, val)
        try:
            self.db.execute(sql)
            self.commit()
            return 1
        except Exception as e:
            logger.info(e)
            return 0


    def get_column(self, column, table_name=table_name, limit=None):
        '''

        :param colums: 一个字符串,字段名
        :param table_name: 一个字符串，表名
        :param limit: 一个整数，查询的数量
        :return: 返回一个列表
        '''
        if not limit:
            sql = "select "+ column+ " from " +table_name +";"
        else:
            sql = ("select "+ column+ " from " +table_name +"limit %d;" %limit)
        self.db.execute(sql)
        result = self.db.fetchall()  # result: ((0,),(1,),(2,),...)
        return [item[0] for item in result]

    def get_counts(self,table_name=table_name):
        '''
        获取数据库指定表的数据量
        :param table_name:表名
        :return: 表中的记录条数
        '''
        sql = "select count(id) from " + table_name +" ;"
        try:
            self.db.execute(sql)
            self.commit()
            result = self.db.fetchall()
            return result[0][0]
        except Exception as e:
            logger.error(e)
            return -1

db = DB()

if __name__ == '__main__':
    db = DB()

    # db.db.execute('drop table if exists zufang;')
    # zufang = '''
    # CREATE TABLE zufang
    # (
    #   id                    int             NOT NULL auto_increment primary key,
    #   city                  char(16)        NOT NULL,
    #   type                  char(16)        NOT NULL,
    #   dist                  char(16)        NOT NULL,
    #   bedroom_num           char(2)         NOT NULL,
    #   hall_num              char(2)         NOT NULL,
    #   bathroom_num          char(2)         NOT NULL,
    #   rent_area             int             NOT NULL,
    #   house_title           varchar(64)     NOT NULL,
    #   resblock_name         char(16)        NOT NULL,
    #   bizcircle_name        char(16)        NOT NULL,
    #   layout                char(32)        NOT NULL,
    #   rent_price_listing    char(6)         NOT NULL,
    #   house_tag             varchar(64)     NOT NULL,
    #   frame_orientation     char(16)        NOT NULL,
    #   m_url                 varchar(128)    NOT NULL unique,
    #   rent_price_unit       char(6)         NOT NULL,
    #   longitude             varchar(32)     NULL,
    #   latitude              varchar(32)     NULL,
    #   distance              varchar(16)     NULL
    # )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'''
    #
    # if db.create_table(zufang) >= 0:          #创建数据表成功
    #     print('table is exists')
    data = {'city': '北京', 'type': '整租', 'dist': '东城', 'bedroom_num': '2',
            'hall_num': '1', 'bathroom_num': '1', 'rent_area': 58,
            'house_title': '整租·六铺炕 2室1厅 南/北', 'resblock_name': '六铺炕',
            'bizcircle_name': '安定门', 'layout': '2室1厅1卫', 'rent_price_listing': '7000',
            'house_tag': '近地铁 集中供暖 随时看房', 'frame_orientation': '南 北',
            'm_url': 'https://m.lianjia.com/chuzu/bj/zufang/BJ2472249267818348544.html',
            'rent_price_unit': '元/月', 'longitude': '116.400533', 'latitude': '39.962226',
            'distance': '2'}

    result = db.insert_data(data)
    print(result)