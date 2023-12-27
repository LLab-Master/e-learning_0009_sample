from flask.json import JSONEncoder
import sqlite3

#DBにアクセスしユーザデータを取得、追加、更新、削除するクラス
class UserManager:

    def __init__(self,dbfilename):
        self.dbfilename = dbfilename

    '''
    ユーザ全件取得
    '''
    def get_user_all(self):
        emp_list = []

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from user";
        cur.execute(sql)
        
        user_list = cur.fetchall()

        con.close()

        return user_list

    '''
    ユーザ1件取得
    '''
    def get_user_one(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from user WHERE id = " + str(id)
        cur.execute(sql)
        
        user = cur.fetchone()
        con.close()

        return user

    '''
    ユーザ追加
    '''
    def add_user(self, User):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = ("insert into user('name', 'password', 'age', 'address') values('"
         + User.name + "','" + User.password + "'," + str(User.age) + ", '" + User.address + "')")

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            print(sql)
            result = False

        con.commit()
        con.close()

        return result

    '''
    ユーザ更新
    '''
    def update_user(self, User):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "UPDATE user SET name = '" + str(User.name) + "'"
        sql += ", password = '" + str(User.password) + "'"
        sql += ", age = " + str(User.age)
        sql += ", address = '" + str(User.address) + "'"
        sql += " WHERE id = " + str(User.id)
        print(sql)
        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result
    '''
    ユーザ削除
    '''
    def delete_user(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "DELETE FROM user WHERE id = "+str(id)

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result

#ユーザクラス
class User():
    id = None
    name = None
    password = None
    age = None
    address = None

    def __init__(self, name=None, password=None, age=None, address=None):
        self.name = name
        self.password = password
        self.age = age
        self.address = address

#Userのセッションに入れるためのエンコーダー
class MyJSONEncoder(JSONEncoder):
    """
    JSON Encoder
    """
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id':obj.id,
                'name': obj.name,
                'password': obj.password,
                'age':obj.age,
                'address': obj.address,
            }
        return super(MyJSONEncoder, self).default(obj)
