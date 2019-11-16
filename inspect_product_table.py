import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='mypass', db='mysql', charset='utf8mb4')
cur = conn.cursor()
cur.execute('USE db')
sql = 'SELECT * FROM products'
cur.execute(sql)
result = cur.fetchall()

for row in result:
    print(row)
