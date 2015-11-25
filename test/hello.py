from distutils.sysconfig import get_python_lib
from MySqlConnect import Connect
print(get_python_lib())

import datetime
import mysql.connector as sql
try:
    conn=sql.Connect(host='127.0.0.1',port='3306',user='ncuser', passwd='1qaz2wsx',database='laohu_user',charset='utf8')
    cursor=conn.cursor()
    query="select * from mobile_app limit 1"
    a=cursor.execute (query)
    for r in cursor:
        print(r)
    connector = Connect(user="root", password="123456", database="laohu_user", host="127.0.0.1", port="3306")
#     result = connector.select(data="app_id,app_key", table="mobile_app", limit="5");
    result = connector.select(table="user", limit="5");
    for res in result:
        print(res)
except sql.Error as e:
    print(e);
