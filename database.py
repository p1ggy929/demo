import pymysql

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'demo'
charset = 'utf8mb4'
connection = pymysql.connect(host=host,port=port,user=user,password=password,database=database,charset=charset)
connection.autocommit(True)

def con_mysql(sql_code):
    try:
        connection.ping(reconnect=True)
        print(sql_code)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_code)
        connection.commit()
        connection.close()
        return cursor

    except pymysql.MySQLError as err_message:
        connection.rollback()
        connection.close()
        return type(err_message),err_message

# 要插入的数据
#username = "admin"
#pwd = "123456"
#code = "INSERT INTO `login_user` (`username`, `password`) VALUES (%s, %s)"
#result = con_mysql(code, (username, pwd))
#print(result)
#connection.close()

#查询插入的数据
#username = "admin"
#password = "123456"
#code = "select * from login_user where username='%s'" % (username)
#cursor_ans = con_mysql(code)
#print(cursor_ans.fetchall())