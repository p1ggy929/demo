import pymysql
import random

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'demo'
charset = 'utf8mb4'
connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)


def get_random_word_and_options():
    try:
        cursor = connection.cursor()
        # 查询表中的总记录数
        count_sql = "SELECT COUNT(*) FROM word"
        cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]

        if total_count < 4:
            print("数据库中数据量不足，无法进行此次测试哦。")
            return None, None, None

        # 随机获取一个word对应的记录索引（用于获取正确答案的word）
        correct_index = random.randint(0, total_count - 1)

        # 获取正确答案对应的word
        correct_word_sql = "SELECT words FROM word LIMIT 1 OFFSET %s"
        cursor.execute(correct_word_sql, (correct_index,))
        correct_word = cursor.fetchone()[0]

        # 获取正确答案对应的explanation
        correct_explanation_sql = "SELECT explanation FROM word LIMIT 1 OFFSET %s"
        cursor.execute(correct_explanation_sql, (correct_index,))
        correct_explanation = cursor.fetchone()[0]

        # 存储已选的索引，避免重复选择（除了正确答案的索引）
        selected_indices = [correct_index]
        options = [correct_explanation]
        while len(options) < 4:
            random_index = random.randint(0, total_count - 1)
            if random_index not in selected_indices:
                selected_indices.append(random_index)
                # 获取随机的explanation作为选项（可能重复，后续处理）
                option_sql = "SELECT explanation FROM word LIMIT 1 OFFSET %s"
                cursor.execute(option_sql, (random_index,))
                option = cursor.fetchone()[0]
                options.append(option)

        # 对选项进行随机打乱，确保正确答案位置随机
        random.shuffle(options)

        return correct_word, options, correct_explanation
    except pymysql.Error as err:
        print(f"数据库查询出错: {err}")
        return None, None, None
    finally:
        cursor.close()