import pymysql
import random

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'demo'
charset = 'utf8mb4'
connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset, autocommit=True)


# 获取所有词库
def get_all_libraries():
    try:
        # 每次查询时重新建立连接
        connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
        cursor = connection.cursor()
        sql = "SELECT id, name FROM word_library"
        cursor.execute(sql)
        libraries = cursor.fetchall()
        print("获取到的词库信息：", libraries)  # 添加调试信息
        return libraries
    except pymysql.Error as err:
        print(f"数据库查询出错: {err}")
        return []
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()


# 随机获取一个 word 以及四个包含正确答案的 explanation 作为选项，根据词库筛选
def get_random_word_and_options(library_id=None):
    try:
        # 每次查询时重新建立连接
        connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
        cursor = connection.cursor()

        if library_id == '':  # 当用户选择"全部词库"时传递空字符串
            library_id = None

        # 根据词库筛选查询表中的总记录数
        if library_id:
            count_sql = "SELECT COUNT(*) FROM unified_word WHERE library_id = %s"
            cursor.execute(count_sql, (library_id,))
        else:
            count_sql = "SELECT COUNT(*) FROM unified_word"
            cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]

        if total_count < 4:
            print("数据库中数据量不足，无法进行此次测试哦。")
            return None, None, None

        # 随机获取一个 word 对应的记录索引（用于获取正确答案的 word）
        correct_index = random.randint(0, total_count - 1)

        # 获取正确答案对应的 word
        if library_id:
            correct_word_sql = "SELECT words FROM unified_word WHERE library_id = %s LIMIT 1 OFFSET %s"
            cursor.execute(correct_word_sql, (library_id, correct_index))
        else:
            correct_word_sql = "SELECT words FROM unified_word LIMIT 1 OFFSET %s"
            cursor.execute(correct_word_sql, (correct_index,))
        correct_word = cursor.fetchone()[0]

        # 获取正确答案对应的 explanation
        if library_id:
            correct_explanation_sql = "SELECT explanation FROM unified_word WHERE library_id = %s LIMIT 1 OFFSET %s"
            cursor.execute(correct_explanation_sql, (library_id, correct_index))
        else:
            correct_explanation_sql = "SELECT explanation FROM unified_word LIMIT 1 OFFSET %s"
            cursor.execute(correct_explanation_sql, (correct_index,))
        correct_explanation = cursor.fetchone()[0]

        # 存储已选的索引，避免重复选择（除了正确答案的索引）
        selected_indices = [correct_index]
        options = [correct_explanation]
        while len(options) < 4:
            random_index = random.randint(0, total_count - 1)
            if random_index not in selected_indices:
                selected_indices.append(random_index)
                # 获取随机的 explanation 作为选项（可能重复，后续处理）
                if library_id:
                    option_sql = "SELECT explanation FROM unified_word WHERE library_id = %s LIMIT 1 OFFSET %s"
                    cursor.execute(option_sql, (library_id, random_index))
                else:
                    option_sql = "SELECT explanation FROM unified_word LIMIT 1 OFFSET %s"
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
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()


def get_random_word(library_id=None):
    try:
        connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
        cursor = connection.cursor()

        if library_id == '':  # 当用户选择"全部词库"时传递空字符串
            library_id = None

        # 根据词库筛选查询表中的总记录数
        if library_id:
            count_sql = "SELECT COUNT(*) FROM unified_word WHERE library_id = %s"
            cursor.execute(count_sql, (library_id,))
        else:
            count_sql = "SELECT COUNT(*) FROM unified_word"
            cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]

        if total_count < 1:
            print("数据库中数据量不足，无法进行此次测试哦。")
            return None

        # 随机获取一个 word 对应的记录索引
        random_index = random.randint(0, total_count - 1)

        # 获取随机的中文内容（假设存储在 chinese_meanings 字段）
        if library_id:
            word_sql = "SELECT explanation FROM unified_word WHERE library_id = %s LIMIT 1 OFFSET %s"
            cursor.execute(word_sql, (library_id, random_index))
        else:
            word_sql = "SELECT explanation FROM unified_word LIMIT 1 OFFSET %s"
            cursor.execute(word_sql, (random_index,))
        chinese_word = cursor.fetchone()[0]

        # 同时获取对应的英文单词（假设存储在 words 字段）
        if library_id:
            english_word_sql = "SELECT words FROM unified_word WHERE library_id = %s LIMIT 1 OFFSET %s"
            cursor.execute(english_word_sql, (library_id, random_index))
        else:
            english_word_sql = "SELECT words FROM unified_word LIMIT 1 OFFSET %s"
            cursor.execute(english_word_sql, (random_index,))
        english_word = cursor.fetchone()[0]

        return chinese_word, english_word
    except pymysql.Error as err:
        print(f"数据库查询出错: {err}")
        return None, None
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()