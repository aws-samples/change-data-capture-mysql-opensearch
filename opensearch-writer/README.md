# opensearch_writer
```
This sample, non-production-ready template.  
© 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.  
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at  
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
```
## Getting started

* this code is tested with python3 

## Requirements   
```
https://aws.amazon.com/serverless/sam/
```
## deploy 

* fix the ARN in the `template.yaml` this AEN need to direct to the AWS Kinesis service 

```
Events:
        KinesisEvents:
          Type: Kinesis # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Stream: <arn of the AWS Kinesis service >
            StartingPosition: LATEST
            BatchSize: 1
            MaximumBatchingWindowInSeconds: 10
            Enabled: true
            ParallelizationFactor: 1
            MaximumRetryAttempts: 1
            BisectBatchOnFunctionError: true
            MaximumRecordAgeInSeconds: 60
            TumblingWindowInSeconds: 0
```

* deployment with sam
```
sam build
sam validate
sam deploy --guided  
```

## show deployment status
```
aws cloudformation describe-stacks |jq -r '.Stacks[] | {StackName,StackStatus}'
```

## cleanup
* delete the deployment (this will only delete the AWS Lambda and trigger)
```
aws cloudformation delete-stack --stack-name opensearch-writer
```
