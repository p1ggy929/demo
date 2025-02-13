from flask import Flask, render_template, request
from login import con_mysql

app = Flask(__name__)


@app.route('/')
def index_login():
    return render_template('login.html')


@app.route("/register")
def index_register():
    return render_template('register.html')


@app.route("/index")
def index_index():
    return render_template('index.html')


@app.route("/Word_Test")
def index_online_learning():
    return render_template('Word_Test.html')


@app.route("/Listening_Learning")
def index_listening_learning():
    return render_template('listening_learning.html')


@app.route("/mine")
def index_mine():
    return render_template('mine.html')


@app.route('/login', methods=["POST"])
def login():
    name = request.form.get('username')
    pwd = request.form.get('password')

    code = "SELECT * FROM login_user WHERE username = %s"
    result = con_mysql(code, (name,))
    if result['status'] == 'success':
        cursor_select = result['data']
        if len(cursor_select) > 0:
            if pwd == cursor_select[0]['password']:
                return render_template('index.html')
            else:
                return '密码错误 <a href="/">返回登录</a>'
        else:
            return '用户不存在 <a href="/">返回登录</a>'
    else:
        return f"查询出错: {result['message']}"


@app.route('/register', methods=["POST"])
def register():
    name = request.form.get('username')
    pwd = request.form.get('password')

    code = "SELECT * FROM login_user WHERE username = %s"
    result = con_mysql(code, (name,))
    if result['status'] == 'success':
        cursor_select = result['data']
        if len(cursor_select) > 0:
            return '用户已存在 <a href="/">返回登录</a>'
        else:
            code = "INSERT INTO `login_user` (`username`, `password`) VALUES (%s, %s)"
            insert_result = con_mysql(code, (name, pwd))
            if insert_result['status'] == 'success':
                return '注册成功 <a href="/">返回登录</a>'
            else:
                return f"注册出错: {insert_result['message']}"
    else:
        return f"查询出错: {result['message']}"


# @app.route('/index', methods=["POST"])
# # def index_index():

if __name__ == '__main__':
    app.run()