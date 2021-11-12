import json
import boto3
import time
import data_index

region='us-east-1' 
client_s3= boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    labels=[]
    for record in event['Records']:
        photos_bucket=record['s3']['bucket']['name']
        name_of_file=record['s3']['object']['key']

    print('reading image: {} from s3 bucket {}'.format(name_of_file, photos_bucket))
    client_rek=boto3.client('rekognition')
    response = client_rek.detect_labels(Image={'S3Object': {'Bucket':photos_bucket,'Name': name_of_file}},MaxLabels=12,MinConfidence=80,)
    print('Detected labels for ' + name_of_file)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        labels.append(label['Name'].lower())
    
    times=time.gmtime()
    time_created=time.strftime("%Y-%m-%dT%H:%M:%S", times)
    print('Image created at {}....'.format(time_created))
    image_obj={'objectKey':name_of_file,'bucket':photos_bucket,'createdTimestamp':time_created,'labels':labels}
    print(str(image_obj))
    es=data_index.connect_to_elastic_search()
    es.index(index="photos", doc_type="_doc", id=time_created, body=image_obj)
    response=es.get(index="photos", doc_type="_doc", id=time_created,refresh=True)
    print(response)
    return response
