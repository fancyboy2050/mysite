import mysql.connector
from mysql.connector import errorcode

class Connect:
    
    def __init__(self, user='', password='', database='', host='127.0.0.1', port='3306'):
        try:
            print("user="+user+", password="+password+", database="+database+", host="+host+", port="+port)
            self._conn = mysql.connector.Connect(user=user,password=password,database=database,host=host,port=port)
            self._cursor = self._conn.cursor()
            print("_init_ ok!")
        except mysql.connector.errors as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('user / password error.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('bad database.')
            else:
                print(err)
    
    def select(self,data='*',table='',where='',limit='',order='',group=''):
        """
                    查询sql语句

        data - 查询的字段，默认 * 或 id,name,email,...
        table - 表名
        where - 查询条件语句
        limit - 结果范围
        order - 排序

        Returns Lists.
        """
        sql = self._sql_contact(data,table,where,limit,order,group)
        print("sql = "+sql)
        result = self._sql_query(data,sql)
        return result

    def get_one(self,data='',table='',where='',order=''):
        """
        获取单行记录

        data - 查询的字段，默认 * 或 id,name,email,...
        table - 表名
        where - 查询条件语句
        order - 排序

        Returns Sets or None.
        """
        sql = self._sql_contact(data,table,where,'1',order)
        result = self._sql_query(data,sql)
        return result[0] if result else None

    def insert(self,data,table):
        """
        新增一条数据

        data - 数据集合 {field:value...}
        table - 表名

        Returns insert_id
        """
        fields = ','.join(data.keys())
        inputs = ','.join(("%s", ) * len(data))
        values = tuple(data.values())
        sql = "INSERT INTO %s (%s) VALUES ("%(table, fields) + inputs + ")"
        self._cursor.execute(sql,values)
        insert_id = self._cursor.lastrowid
        self._conn.commit()
        return insert_id

    def insert_many(self,data,table):
        """
        新增多条数据

        data - 数据列表 [{field:value...}...]
        table - 表名

        Returns rowcount 影响到行数
        """
        fields = ','.join(data[0].keys())
        inputs = ','.join(("%s", ) * len(data[0]))
        values = []
        [values.append(tuple(item.values())) for item in data]

        sql = "INSERT INTO %s (%s) VALUES ("%(table, fields) + inputs + ")"
        self._cursor.executemany(sql,values)
        insert_id = self._cursor.lastrowid
        self._conn.commit()
        return self._cursor.rowcount

    def update(self,data,table,where):
        """
        修改数据

        data - 数据集合 {field:value...}
        table - 表名
        where - 条件

        Returns rowcount 影响到行数
        """
        fields = (",".join(map(lambda k: k+"=%s", data.keys())))
        values = tuple(data.values())
        sql = "UPDATE %s SET "%table + fields + " WHERE " + where
        self._cursor.execute(sql,values)
        self._conn.commit()
        return self._cursor.rowcount

    def delete(self,table,where):
        """
        删除数据

        table - 表名
        where - 条件

        Returns rowcount 影响到行数
        """
        where = ' WHERE '+where if where else ''
        sql = 'DELETE FROM ' + table + where
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.rowcount

    def close(self):
        """关闭游标和数据库连接"""
        self._cursor.close()
        self._conn.close()

    def _sql_contact(self,data='',table='',where='',limit='',order='',group=''):
        """构造和拼接sql语句"""
        where = ' WHERE '+where if where else ''
        limit = ' LIMIT '+limit if limit else ''
        order = ' ORDER BY '+order if order else ''
        group = ' GROUP BY '+group if group else ''
        data = data if data else '*'
        sql = 'SELECT '+data+' FROM ' + table + where + group + order +limit
        return sql

    def _sql_query(self,data,sql):
        """执行sql并返回结果集"""
        self._cursor.execute(sql)
        result = []
        column_names = self._cursor.column_names if data=='*' else tuple(data.split(','))
        for res in self._cursor.column_names:
            print("res = "+res)   
        [result.append(dict(zip(column_names,item))) for item in self._cursor]
        return result
        