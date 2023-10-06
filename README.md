# CDC-Pipeline-with-near-real-time-capability
**Implement upstream data changes with near real time capability using CDC on AWS.**

# 1-Introduction
**Change Data Capture (CDC)** is a technique used in databases and data integration systems to **identify and track** changes made to data. It's especially valuable in scenarios where you need to **replicate** data from one source to another or monitor **real-time** changes in a database.
**But WHY CDC Pipeline is Important?**
1- CDC is essential for monitoring and providing **operational insights**. It enables organizations to track and analyze changes in their systems, which can be valuable for **troubleshooting, auditing, and compliance.**
2- CDC pipelines allow organizations to capture and process data changes as they occur in source systems in **real time or near real time**. Data engineers can feed updated data **directly into data warehouses, data lakes, or analytical systems,** ensuring that business analysts and data scientists work with **the most current information.** 

**In this project we will have the capability to :**
- [ ] **Tracking changes made at Users Informations Database in near real time using CDC.**
- [ ] **Configure CDC replication.**
- [ ] **Implement upstream data changes with neat real time capability.**

# 2-Architecture 
![architecture](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/74e40af7-7e7f-43c4-9fa7-5bd4d2356ea5)
- [ ] **Amazon Aurora MySQL compatible database** : It's a relational managed database provided by AWS with high performance with low latency and is designed for demanding, production-grade workloads, offering high scalability, and reliability. I choosed Aurora for this project because It provides read and write scalability by supporting up to 15 read replicas, which can help distribute read traffic and improve read performance which is the most use case for CDC pipelines. This database will be our **upstream datastore**.
- [ ]  **AWS Data Migration Service DMS** : It's a fully managed database migration service provided by AWS. It enables you to migrate databases from various source data stores to AWS data stores securely and with minimal downtime. In our project, I will send CDC information to amazon Kinesis Data Streams.
- [ ]  **AWS Kinesis Data Streams** : It's a massively scalable and durable data streaming service that can collect and process large streams of data records in near real time, this allows upstream data changes to be made available downstream with low latency.
- [ ]  **AWS Glue** : It's a fully managed **ETL** service to stream data from Kinesis data stream, mask PII found in our change data capture, and store the transformed data in S3 bucket.
- [ ]  **AWS S3 bucket** : It will be our storage service for transformed data.
- [ ]  **AWS Athena** : for analyzing data stored in Amazon S3 using standard SQL.


**Let's dive down into details to see how to implement this architecture!!**

# 3-Steps and Requirements

In this project, I used a simple dataset that contain Informations about users such as : userid, username, firstname, lastname, city, state, numberofdocuments, and some **sensitive data** as : phone and email. Our ETL transformation will ensure to **hide** those PII. 

# 4-Prepare Our EC2 instance 
**Packages and Installation reuqired** 
- [ ] Python3 of course !
- [ ] boto3 : to interacte with AWS services
- [ ] mysql-connector-python + mysql client core 8.0 : to establish connexion between our Database and EC2 instance.
- [ ] amazon-kineis-client : amazon_kclpy in order to execute our reading from kinesis on EC2 instance.
- [ ] Files loaded on EC2 instance : load file to ec2: users.csv, commands.sql, read_kinesis_first_10_records.py, aurora_update_single_row.py, aurora_update_multiple_row.py, read_kinesis_update.py
![EC2 required installation](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/65a1e805-af28-44c3-99bd-7e986c5fc49e)
![EC2 required installation 2 ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/0203a3b8-1094-45f5-b4a7-d6f27bfd0f50)




