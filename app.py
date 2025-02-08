from flask import Flask, render_template,request
from database import con_mysql
app = Flask(__name__)

login_data = {
    "admin":"123456"
}
@app.route('/')
def index_login():  # put application's code here
    return render_template('login.html')

@app.route("/register")
def index_register():
    return render_template('register.html')



@app.route('/login',methods=["post"])
def login():
    name = request.form.get('username')
    pwd = request.form.get('password')

    code = "select * from login_user where username = '%s'" % (name)
    cursor_ans = con_mysql(code)
    cursor_select = cursor_ans.fetchall()
    if len(cursor_select) > 0:
        if pwd == cursor_select[0]['password']:
            return "登录成功"
        else:
            return '密码错误 <a href="/">返回登录</a>'
    else:
        return '用户不存在 <a href="/">返回登录</a>'


@app.route('/register',methods=["post"])
def register():
    name = request.form.get('username')
    pwd = request.form.get('password')

    code = "select * from login_user where username = '%s'" % (name)
    cursor_ans = con_mysql(code)
    cursor_select = cursor_ans.fetchall()
    if len(cursor_select) > 0:
       return '用户已存在 <a href="/">返回登录</a>'
    else:
        code = "INSERT INTO `login_user` (`username`, `password`) VALUES (%s, %s)" % (name, pwd)
        con_mysql(code)
        return '注册成功 <a href="/">返回登录</a>'


if __name__ == '__main__':
    app.run()

