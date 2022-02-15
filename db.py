import pymysql

def db():
    return pymysql.connect(
        host='127.0.0.1', 
        user='root', 
        password='abcdefg',
        db='war-game', 
        charset='utf8')
