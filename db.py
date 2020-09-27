import pymysql

db = pymysql.connect(host='localhost', user='root', password='root', database='doubanbook', port=3306,
                     charset='utf8mb4')


def check_data(book_id):
    sql = "select count(*) from book_info where book_id=%s" % (book_id,)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
    except:
        db.ping()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
    if res == (0,):
        return True
    else:
        return False


def save_book_info(kwargs):
    data = kwargs
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    sql = "insert into book_info (%s) values (%s)" % (keys, values)
    try:
        cursor = db.cursor()
        cursor.execute(sql, tuple(data.values()))
    except:
        db.ping()
        cursor = db.cursor()
        cursor.execute(sql, tuple(data.values()))
    db.commit()
    cursor.close()
    db.close()


def save_book_content(content, book_id):
    title_list = content.split('\n')
    val = [(title.strip(), book_id) for title in title_list]
    sql = "insert into book_content (content,book_id) values (%s,%s)"
    try:
        cursor = db.cursor()
        cursor.executemany(sql, val)
    except:
        db.ping()
        cursor = db.cursor()
        cursor.executemany(sql, val)
    db.commit()
    cursor.close()
    db.close()


def save_book(item):
    data = item
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    sql = "insert into book_list (%s) values (%s)" % (keys, values)
    try:
        cursor = db.cursor()
        cursor.execute(sql, tuple(data.values()))
    except:
        db.ping()
        cursor = db.cursor()
        cursor.execute(sql, tuple(data.values()))
    db.commit()
    cursor.close()
    db.close()


def check_book(book_id):
    sql = "select count(*) from book_list where book_id=%s" % (book_id,)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
    except:
        db.ping()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()

    if res == (0,):
        return True
    else:
        return False


def update_info(book_id, book_info):
    sql = "update book_list set book_info=%s where book_id=%s"
    try:
        cursor = db.cursor()
        cursor.execute(sql, (book_info,book_id))
    except:
        db.ping()
        cursor = db.cursor()
        cursor.execute(sql, (book_info,book_id))
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    print(check_data('26280552'))
