import json
import requests
import boto3
import data_index

def lambda_handler(event, context):
    print(event)
    lex_client=boto3.client('lex-runtime')
    q=event["queryStringParameters"]["q"]
    lex_resp=lex_client.post_text(botName='NLPControlledPhotoAlbum',botAlias='photoalbum',userId='Twisha',inputText=q)
    print("LEX RESPONSE --- {}".format(json.dumps(lex_resp)))
    q=lex_resp['slots']['searchque']
    print('query', q)
    keys=q.split(',')
    Result=[]
    es=data_index.connect_to_elastic_search()
    ot=[]
    o=[]
    oS=""
    oRs=[]
    print('keys',keys)
    for i in range(len(keys)):
        print(keys[i])
        print(es.info())
        qu = {"size":25, "query":{"match":{"labels": str(keys[i].lower())}}}
        res = es.search(body=json.dumps(qu))
        print(res)
        Result.append(res)
        print("Got %d Hits:" % res['hits']['total']['value'])
        print(res)
        for i in res['hits']['hits']:
            bucket = i['_source']['bucket']
            image = i['_source']['objectKey']
            a = "https://s3.amazonaws.com/" + bucket + "/" + image
            if a not in o:
                o.append(a)
                ot.append({"url":a,"labels":i['_source']['labels']})
                oS += a + ", "
                oRs.append({'title': image.split(".")[0], 'attachmentLinkUrl': a, 'imageUrl': a})
        print('File path: ', ot) 
    return {'statusCode': 200,'body': json.dumps(ot),'headers': {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'}}
