# mysql_cdc
```
This sample, non-production-ready template.  
© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
```

## Getting started

* this code hes bin tested with python3 (3.9)

## Requirements   
```
pip3 install -r requirements.txt
```
### Creating replication user for dcd 
```
CREATE USER 'repl'@'%' IDENTIFIED  BY 'slavepass';
GRANT REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'repl'@'%';
GRANT REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'repl'@'%'
```

### MySQL config 
```
[mysqld]
server-id		 = 1
log_bin			 = /var/log/mysql/mysql-bin.log
expire_logs_days = 10
max_binlog_size  = 100M
binlog-format    = row #Very important if you want to receive write, update and delete row events
```




## Test the replication 

```
use test;
XA START 'xatest';
INSERT INTO test5 (data,data2) VALUES ("Hello", "World");
XA END 'xatest';
XA PREPARE 'xatest';
XA COMMIT 'xatest';


```
## Test the AWS OpenSearch service

```
 curl -XGET -u 'root:Aa123456!' 'https://vpc-opensearchdomain-testurl.us-east-1.es.amazonaws.com/mysql_data/_doc/51' |jq
```

