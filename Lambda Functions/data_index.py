from requests_aws4auth import AWS4Auth
import boto3
from elasticsearch import Elasticsearch
from opensearchpy import OpenSearch, RequestsHttpConnection

host = 'search-photos-wvfh6jkklbdjkvfwd2n5ijnwne.us-east-1.es.amazonaws.com'
region = 'us-east-1' 
ACCESS_KEY = 'AKIAXUFDT3OUQPH5EXUB'
SECRET_KEY = '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'

def authenticate_user(service):
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region, service)
    return awsauth
    
def connect_to_elastic_search():
    service = 'es'
    awsauth = authenticate_user(service)
    es = OpenSearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )
    print(es.info())
    return es
