from flask import Flask, render_template, request
from login import con_mysql
from word_test import get_random_word_and_options, get_all_libraries
import datetime

app = Flask(__name__)

total_count = 0  # 总回答数量
correct_count = 0  # 正确回答数量
start_time = None  # 记录开始时间

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
    global total_count, correct_count, start_time
    message = None
    libraries = get_all_libraries()

    # 从 URL 参数中获取用户选择的词库 ID，如果没有选择则默认为 None
    selected_library_id = request.form.get('library_id') if request.method == 'POST' else request.args.get('library_id')

    if selected_library_id:
        try:
            selected_library_id = int(selected_library_id)
            if start_time is None:
                start_time = datetime.datetime.now().replace(microsecond=0)  # 选择词库时记录开始时间
        except ValueError:
            message = "选择的词库 ID 无效，请重新选择。"

    correct_word, options, correct_explanation = get_random_word_and_options(selected_library_id)

    if request.method == 'POST':
        user_choice = request.form.get('choice')
        prev_correct_explanation = request.form.get('correct_explanation')
        prev_options = request.form.getlist('options')
        if user_choice is None:
            message = "请选择一个选项。"
        else:
            try:
                choice_index = int(user_choice) - 1
                if 0 <= choice_index < 4 and prev_options[choice_index] == prev_correct_explanation:
                    message = "回答正确！"
                    correct_count += 1  # 回答正确，正确数量加一
                else:
                    message = f"回答错误，正确的解释：{prev_correct_explanation}"
                total_count += 1  # 总回答数量加一
            except ValueError:
                message = "请输入有效的整数选项序号哦。"

    if correct_word and options:
        # 计算正确率
        accuracy = correct_count / total_count * 100 if total_count > 0 else 0
        # 计算已用时间
        elapsed_time = (datetime.datetime.now().replace(microsecond=0) - start_time).total_seconds() if start_time else 0
        elapsed_time_str = str(datetime.timedelta(seconds=elapsed_time))

        # 在渲染模板时传递所选词库的信息和统计数据
        return render_template('word_test.html', correct_word=correct_word, options=options,
                               correct_explanation=correct_explanation, message=message,
                               libraries=libraries, selected_library_id=selected_library_id,
                               total_count=total_count, correct_count=correct_count, accuracy=accuracy,
                               elapsed_time=elapsed_time_str)
    if selected_library_id:
        for library in libraries:
            if library[0] == selected_library_id:
                return f"词库 '{library[1]}' 中数据量不足，无法进行此次测试哦。"
    return "请先选择一个词库并点击应用"


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(debug=True)