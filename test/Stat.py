from MySqlConnect import Connect

import mysql.connector as sqlConnector

try:
    connector = Connect(user="bookAdmin", password="bookAdmin", database="173", host="10.3.254.97", port="3307")
    result = connector.select(table="mobile_app", limit="5");
    for res in result:
        print(res)
except sqlConnector.Error as e:
    print(e);