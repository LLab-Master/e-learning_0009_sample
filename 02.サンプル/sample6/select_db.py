import sqlite3

dbfilename = './flask_test.db'

con = sqlite3.connect(dbfilename)
cur = con.cursor()

sql = "select * from user"

cur.execute(sql)

users = cur.fetchall()

print('ID 氏名 パスワード 年齢 住所')
print('-'*34)

for usr in users:
    print(str(usr[0]) + " , " + str(usr[1]) + " , " + str(usr[2]) + " , " + str(usr[3]) + " , " + str(usr[4]))

print('-'*34)


con.commit()
con.close()