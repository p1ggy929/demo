import pymysql

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'demo'
charset = 'utf8mb4'
connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
connection.autocommit(False)


def con_mysql(sql_code, values=None):
    try:
        connection.ping(reconnect=True)
        print(sql_code)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        if values:
            cursor.execute(sql_code, values)
        else:
            cursor.execute(sql_code)
        connection.commit()
        result = cursor.fetchall()
        return {
            'status': 'success',
            'data': result
        }
    except pymysql.MySQLError as err_message:
        connection.rollback()
        return {
            'status': 'error',
            'message': f'{type(err_message)}: {err_message}'
        }