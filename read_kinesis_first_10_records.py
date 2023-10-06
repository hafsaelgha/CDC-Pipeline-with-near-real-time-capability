import boto3

#Client for kinesis
kinesis_client = boto3.client('kinesis',
    aws_access_key_id='AKIAVJ77NPSASCETFDXK',
    aws_secret_access_key='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',
    region_name='us-east-1'
)

#Stream name 
stream_name = 'kinesis-aurora'

#Number of records to read
num_records_to_read = 10

#Acess to the Shard Iterator
shard_iterator = kinesis_client.get_shard_iterator(
    StreamName=stream_name,
    ShardId='shardId-000000000001',  
    ShardIteratorType='TRIM_HORIZON' 
)['ShardIterator']

#Read records
record_count = 0
while record_count < num_records_to_read:
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,
        Limit=num_records_to_read - record_count
    )
    records = response['Records']
    
    for record in records:
        data = record['Data']
        #Transform data record 
        print(f"Record {record_count + 1}: {data.decode('utf-8')}")
        record_count += 1
    
    shard_iterator = response['NextShardIterator']

    if not shard_iterator:
        break

#Disconnect
kinesis_client.close()

