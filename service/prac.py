import psycopg2
import pdb
import os
import json
import pdb
from psycopg2.extras import Json

connection = psycopg2.connect(database="flask_notifications", user="everblue", password="mypass", host="127.0.0.1", port="5432")
cursor = connection.cursor()
data = []

sql = "SELECT timestamp from jsonfile"
cursor.execute(sql)
result = cursor.fetchall()
exist_list = []
for row in result:
    exist_list.append(row[0])
print(exist_list)    

for path in os.listdir('logs'):
    if 'json' in path:
        timestamp = path[:8]
        if timestamp not in exist_list:
            with open('logs/{}'.format(path)) as f:
                for row in f:
                    records = row.split('\t', 2)
                    data.append((records[0], Json(json.loads(records[2].strip()))))
                sql = "INSERT INTO product (timestamp, data) VALUES (%s, %s)"
                cursor.executemany(sql, data)
                connection.commit()
            sql = "INSERT INTO jsonfile (timestamp) VALUES (%s)"
            cursor.execute(sql, (timestamp,))
            connection.commit()
        else:
            print(timestamp + ' in the list')

#for item in data:
    #my_data = [item[field] for field in fields]
    #insert_query = "INSERT INTO crm VALUES (%s, %s, %s, %s)"
    #cursor.execute(insert_query, tuple(my_data))
    #print(item)
    #break
