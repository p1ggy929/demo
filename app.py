from flask import Flask, render_template, request
from login import con_mysql
from word_test import get_random_word_and_options

app = Flask(__name__)


@app.route('/')
def index_main():
    return render_template('index.html')


@app.route("/index")
def index_index():
    return render_template('index.html')


@app.route("/register")
def index_register():
    return render_template('register.html')


@app.route("/login")
def index_login():
    return render_template('login.html')


@app.route("/Word_Test")
def index_word_test():
    return render_template('word_test.html')


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
                return '密码错误 <a href="/login">返回登录</a>'
        else:
            return '用户不存在 <a href="/login">返回登录</a>'
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
            return '用户已存在 <a href="/login">返回登录</a>'
        else:
            code = "INSERT INTO `login_user` (`username`, `password`) VALUES (%s, %s)"
            insert_result = con_mysql(code, (name, pwd))
            if insert_result['status'] == 'success':
                return '注册成功 <a href="/login">返回登录</a>'
            else:
                return f"注册出错: {insert_result['message']}"
    else:
        return f"查询出错: {result['message']}"


@app.route('/index', methods=["POST"])
def index():
    if request.method == "POST":
        return render_template('login.html')


@app.route('/word_test', methods=['GET', 'POST'])
def word_test():
    message = None
    correct_word, options, correct_explanation = get_random_word_and_options()
    if request.method == 'POST':
        user_choice = request.form.get('choice')
        prev_correct_explanation = request.form.get('correct_explanation')
        prev_options = request.form.getlist('options')
        try:
            choice_index = int(user_choice) - 1
            if 0 <= choice_index < 4 and prev_options[choice_index] == prev_correct_explanation:
                message = "回答正确！"
            else:
                message = f"回答错误，正确的解释：{prev_correct_explanation}"
        except ValueError:
            message = "请输入有效的整数选项序号哦。"

    if correct_word and options:
        return render_template('word_test.html', correct_word=correct_word, options=options,
                               correct_explanation=correct_explanation, message=message)
    return "数据库中数据量不足，无法进行此次测试哦。"


if __name__ == '__main__':
    app.run()