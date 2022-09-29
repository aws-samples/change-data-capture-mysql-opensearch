#This sample, non-production-ready template.  
#© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
#This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
#http://aws.amazon.com/agreement or other written agreement between Customer and either
#Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.


import boto3
import json
from datetime import datetime
import time
from botocore.exceptions import ClientError

my_stream_name = 'mysql_data'

kinesis_client = boto3.client('kinesis')


response = kinesis_client.describe_stream(StreamName=my_stream_name)
print(response)
my_shard_id = "shardId-000000000003"
#= response['StreamDescription']['Shards'][0]['ShardId']
max_records = 10000
try:
    response = kinesis_client.get_shard_iterator(
        StreamName=my_stream_name, ShardId=my_shard_id,
        ShardIteratorType='LATEST')
    print(my_shard_id)
    shard_iter = response['ShardIterator']
    record_count = 0
    while record_count < max_records:
        response = kinesis_client.get_records(
            ShardIterator=shard_iter, Limit=10)
        shard_iter = response['NextShardIterator']
        records = response['Records']
        print("Got %s records.", len(records))
        record_count += len(records)
        print(records)
except ClientError:
    print("Couldn't get records from stream %s.", my_stream_name)
    raise
