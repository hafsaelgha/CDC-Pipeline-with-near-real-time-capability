# CDC-Pipeline-with-near-real-time-capability
Implement upstream data changes with near real time capability using CDC on AWS

# 1-Introduction
**Change Data Capture (CDC)** is a technique used in databases and data integration systems to **identify and track** changes made to data. It's especially valuable in scenarios where you need to **replicate** data from one source to another or monitor **real-time** changes in a database.
In this project we will have the capability to : 
- [ ] Tracking changes made at Users Informations Database in near real time using CDC.
- [ ] Configure CDC replication
- [ ] Implement upstream data changes with neat real time capability

# 2-Architecture 
![architecture](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/74e40af7-7e7f-43c4-9fa7-5bd4d2356ea5)
- [ ] Amazon Aurora MySQL compatible database : It's a relational managed database provided by AWS with high performance with low latency and is designed for demanding, production-grade workloads, offering high scalability, and reliability. I choosed Aurora for this project because It provides read and write scalability by supporting up to 15 read replicas, which can help distribute read traffic and improve read performance which is the most use case for CDC pipelines. This database will be our **upstream datastore**.
- [ ]  AWS Data Migration Service DMS : It's a fully managed database migration service provided by AWS. It enables you to migrate databases from various source data stores to AWS data stores securely and with minimal downtime. In our project, I will send CDC information to amazon Kinesis Data Streams.
- [ ]  AWS Kinesis Data Streams : It's a massively scalable and durable data streaming service that can collect and process large streams of data records in near real time, this allows upstream data changes to be made available downstream with low latency.
- [ ]  AWS Glue : It's a fully managed **ETL** service to stream data from Kinesis data stream, mask PII found in our change data capture, and store the transformed data in S3 bucket.
- [ ]  AWS S3 bucket : It will be our storage service for transformed data.
- [ ]  AWS Athena : for analyzing data stored in Amazon S3 using standard SQL.


**Let's dive down into details to see how to implement this architecture!!**

# 3-Steps and Requirements




