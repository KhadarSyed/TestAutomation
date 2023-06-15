# Getting the credentials from the es_config.txt file
d = {i.split('=')[0]:i.split('=')[1] for i in  [line.rstrip() for line in open('./es_config.txt')]}


# Importing required packages
try:
    from elasticsearch import Elasticsearch
    import boto3

except Exception as e:
    print(f"Error occured while importing required packages - {e}")

# Creating ES and s3 client
try:
    es = Elasticsearch(d['ES_HOST'], basic_auth=('elastic',d['ES_PASSWORD']))
    session = boto3.Session(aws_access_key_id=d['AWS_ACCESS_KEY_ID'], aws_secret_access_key=d['AWS_SECRET_ACCESS_KEY'])
    s3 = session.client('s3')
except Exception as e:
    print(f"Error occured while creating ES/S3 client - {e}")

# Get list of objects in bucket

response = s3.list_objects_v2(Bucket=d['BUCKET_NAME'])
files = []
for obj in response['Contents']:
    files.append(obj['Key'])

if es.indices.exists(index="amx"):
    for i in range(10,15):
        response = s3.get_object(Bucket=d['BUCKET_NAME'], Key=files[i])
        json_data = response['Body'].read().decode('utf-8')
        # Load JSON data to Elasticsearch
        es.index(index='amx', body=json_data, timeout=30)
else:
    es.indices.create(index='amx',ignore=400)
    for i in range(10,15):
        response = s3.get_object(Bucket=d['BUCKET_NAME'], Key=files[i])
        json_data = response['Body'].read().decode('utf-8')
        # Load JSON data to Elasticsearch
        es.index(index='amx', body=json_data, timeout=30)




