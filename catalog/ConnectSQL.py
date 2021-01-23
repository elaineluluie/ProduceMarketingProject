from pymysql import cursors, connect

# 連線資料庫
def SQLconnect():
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)

def SQLquery(String query):
        with conn.cursor() as cur:
            sql = query
            cur.execute(sql)
            conn.commit()
            return cur
        conn.close()
