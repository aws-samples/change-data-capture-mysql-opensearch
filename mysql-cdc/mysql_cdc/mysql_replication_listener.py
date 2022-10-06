#This sample, non-production-ready template .  
#© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
#This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
#http://aws.amazon.com/agreement or other written agreement between Customer and either
#Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.


#
# Dump all replication events from a remote mysql server
# pip install mysql-replication boto3 requests
#
import requests
import secrets
import boto3
import json
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)




def get_secrets(version=None):
    '''
    Gets the value of a secret.
    Version (if defined) is used to retrieve a particular version of
    the secret.
    '''
    instance_region = get_instance_region()
    secrets_client = boto3.client('secretsmanager',region_name=instance_region)
    kwargs = {'SecretId': "awsblog/mysql/replication"}
    if version is not None:
        kwargs['VersionStage'] = version
    response = secrets_client.get_secret_value(**kwargs)
    response_json = json.loads(response['SecretString'])
    return(response_json)

'''
Get the ec2 instance region from local context
'''
def get_instance_region():
    instance_identity_url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
    session = requests.Session()
    r = requests.get(instance_identity_url)
    response_json = r.json()
    region = response_json.get("region")
    return(region)

def main():
    instance_region = get_instance_region()
    mysql_secret_json = get_secrets()
    kinesis = boto3.client("kinesis",region_name=instance_region)
    
    MYSQL_SETTINGS = {
      "host": mysql_secret_json['host'],
      "port": 3306,
      "user": mysql_secret_json['username'],
      "passwd": mysql_secret_json['password']
      }
    '''
    * server_id is your slave identifier, it should be unique.
    * set blocking to True if you want to block and wait for the next event at
    the end of the stream
    * only_events will listen only to describes events 
    '''
    print(">>>listener start streaming to:mysql_data")
    stream = BinLogStreamReader(connection_settings=MYSQL_SETTINGS,
                                server_id=1012598212,
                                blocking=True,
                                resume_stream=True,
                                only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])
    for binlogevent in stream:
        for row in binlogevent.rows:
            print(">>> start event")
            event = {"schema": binlogevent.schema,
                    "table": binlogevent.table,
                    "type": type(binlogevent).__name__,
                    "row": row
                    }
            print(">>>event",event)
            output = kinesis.put_record(StreamName="mysql_data", Data=json.dumps(event), PartitionKey="default")
            print(">>kinasis output",output)

            #binlogevent.dump()




    stream.close()


if __name__ == "__main__":
    main()

