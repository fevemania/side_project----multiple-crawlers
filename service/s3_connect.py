import boto3
import os

s3 = boto3.resource('s3')

objects = s3.meta.client.list_objects_v2(Bucket='dataforcrawl')
if objects.get('Contents') is not None:
    filename = objects['Contents'][0]['Key']
    dirname = filename.split('/')[0]
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    
for obj in objects['Contents']:
    if not os.path.isfile(obj['Key']):
        s3.meta.client.download_file('dataforcrawl', obj['Key'], obj['Key'])
