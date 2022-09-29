#This sample, non-production-ready template .  
#© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
#This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
#http://aws.amazon.com/agreement or other written agreement between Customer and either
#Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.


#
# Dump all replication events from a remote mysql server
# pip install mysql-replication boto3
#
import boto3
import json
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)


MYSQL_SETTINGS = {
"host": "hostname",
      "port": 3306,
      "user": "repl",
      "passwd": "******"
      }


def main():

    kinesis = boto3.client("kinesis")

    # server_id is your slave identifier, it should be unique.
    # set blocking to True if you want to block and wait for the next event at
    # the end of the stream
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
