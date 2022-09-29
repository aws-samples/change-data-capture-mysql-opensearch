#This sample, non-production-ready template.  
#© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
#This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
#http://aws.amazon.com/agreement or other written agreement between Customer and either
#Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.


import base64
import boto3
import json
import requests
from requests.auth import HTTPBasicAuth 

region = 'us-east-1' # e.g. us-west-1
service = 'es'

index = 'mysql_data'
type = '_doc'

headers = { "Content-Type": "application/json" }

def get_secrets(version=None):
    '''
    Gets the value of a secret.
    Version (if defined) is used to retrieve a particular version of
    the secret.
    '''
    secrets_client = boto3.client('secretsmanager')
    kwargs = {'SecretId': "awsblog/opensearch/writer"}
    if version is not None:
        kwargs['VersionStage'] = version
    response = secrets_client.get_secret_value(**kwargs)
    response_json = json.loads(response['SecretString'])
    return(response_json)



def lambda_handler(event, context):
    elastic_secret = get_secrets()
    host = elastic_secret['hosturi'] # the OpenSearch Service domain, including https://
    url = host + '/' + index + '/' + type + '/'
    
    print("START...")
    count = 0
    for record in event['Records']:
        #id = record['eventID']
        timestamp = record['kinesis']['approximateArrivalTimestamp']
        # Kinesis data is base64-encoded, so decode here
        message = base64.b64decode(record['kinesis']['data'])
        message_json = json.loads(message)
        print("message",message_json)
        op_type = message_json['type']
        if op_type == ('WriteRowsEvent'):
            id = str(message_json['row']['values']['id'])
        else:
            id = str(message_json['row']['after_values']['id'])
            
        # Create the JSON document
        document = { "id": id, "timestamp": timestamp, "message": message }

        # Index the document
        r = requests.put(url + id, auth=HTTPBasicAuth(elastic_secret['user'], elastic_secret['password']), json=document, headers=headers)
        count += 1
        print("document",document)
        print("requests",r)
        print("URL",url + id)
        print("END")
    return 'Processed ' + str(count) + ' items.'
