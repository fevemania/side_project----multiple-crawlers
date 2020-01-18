import psycopg2
import socket
import os
import json
from psycopg2.extras import Json
import boto3
import pytz
import dateutil.parser
from datetime import datetime
from datetime import timedelta

timestamp_filename = 'log/last_time_of_s3_jsonfile_to_postgres.txt'
if not os.path.exists(os.path.dirname(timestamp_filename)):
    os.makedirs(os.path.dirname(timestamp_filename))

if not os.path.isfile(timestamp_filename):
    #now_utc = pytz.utc.localize(datetime.utcnow())
    now_utc = pytz.utc.localize(dateutil.parser.parse('2019-01-01T00:00:00'))
    #newest_modified = last_modified = now_utc.replace(microsecond=0)
    newest_modified = last_modified = now_utc.date()
    with open(timestamp_filename, 'w') as f:
        f.write(str(last_modified))
else:
    with open(timestamp_filename, 'r') as f:
        newest_modified = last_modified = dateutil.parser.parse(f.read()).date()

s3 = boto3.resource('s3')
objects = s3.meta.client.list_objects_v2(Bucket='dataforcrawl')

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
cursor = connection.cursor()

# select exist date from Date
existed_date_set = set()
cursor.execute('select date from dates')
result = cursor.fetchall()
for row in result:
    existed_date_set.add(row[0])

if objects.get('Contents') is not None:
    dirname = objects['Contents'][0]['Key'].split('/')[0]
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    for obj in objects['Contents']:
        path = obj['Key']
        if obj['LastModified'].date() > last_modified and path.endswith('.json'):
            if obj['LastModified'].date() > newest_modified:
                newest_modified = obj['LastModified'].date()
            data = []
            distinct_date_list = []
            s3.meta.client.download_file('dataforcrawl', path, path)
            with open(path, 'r') as f:
                for row in f:
                    records = row.split('\t', 2)
                    now_utc = dateutil.parser.parse(records[0])
                    date = now_utc.date()
                    if date not in existed_date_set:
                        distinct_date_list.append((date,))
                        existed_date_set.add(date)

                    json_data = records[2].strip().replace('\\u0000', '')
                    try:
                        json_data1 = json.loads(json_data)
                        name = json_data1['item']['name']
                        data.append((Json(json.loads(json_data)), name, now_utc.date()))
                    except:
                        pass  # json_data1 = {'item': None, 'version': 'xxxx', 'data': None, 'error_msg': None, 'error': -1}
                
                if distinct_date_list:
                    for new_date_tuple in distinct_date_list:
                        new_date = new_date_tuple[0]
                        tablename = 'product_{}'.format(new_date)
                        cursor.execute("CREATE TABLE \"{}\" PARTITION OF product FOR VALUES FROM ('{}') TO ('{}')".format(
                            tablename, new_date, new_date + timedelta(days=1)))
                        connection.commit()
                    cursor.executemany("INSERT INTO dates (date) VALUES (%s)", distinct_date_list)
                    connection.commit()

                sql = "INSERT INTO product (data, name, date) VALUES (%s, %s, %s)"
                cursor.executemany(sql, data)
                connection.commit()

            os.remove(path)
            print('finish store {} into postgres'.format(path))

    if newest_modified != last_modified:
        with open(timestamp_filename, 'w') as f:
            f.write(str(newest_modified))

cursor.close()
connection.close()
