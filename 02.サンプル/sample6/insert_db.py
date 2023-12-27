import sqlite3

dbfilename = './flask_test.db'

con = sqlite3.connect(dbfilename)
cur = con.cursor()

sql = "insert into user('name', 'password', 'age', 'address') values('Taro', 'abc', 30, 'Tokyo'),"
sql += "('Jiro', 'def', 23, 'Osaka'),"
sql += "('Hanako', 'hij', 44, 'Yokohama'),"
sql += "('Ken', 'klm', 35, 'Nagoya'),"
sql += "('Tom', 'xzy', 33, 'Sapporo');"

cur.execute(sql)

con.commit()
con.close()