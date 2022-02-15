import pymysql


def db():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='abcdefu',
        db='war-game',
        charset='utf8'
    )
