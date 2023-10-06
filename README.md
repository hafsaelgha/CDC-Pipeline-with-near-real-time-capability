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
- [ ] amazon-kinesis-client : amazon_kclpy in order to execute our reading from kinesis on EC2 instance.
- [ ] Files loaded on EC2 instance : load file to ec2: users.csv, commands.sql, read_kinesis_first_10_records.py, aurora_update_single_row.py, aurora_update_multiple_row.py, read_kinesis_update.py
![EC2 required installation](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/65a1e805-af28-44c3-99bd-7e986c5fc49e)
![EC2 required installation 2 ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/0203a3b8-1094-45f5-b4a7-d6f27bfd0f50)

# 5-Create Amamzon Aurora MySQL compatible database from RDS

## Parameter Group 
Fisrt, **The binlog** is a log file in MySQL that records all changes **(inserts, updates, deletes)** made to the database. It acts as a chronological record of every data modification operation.
Before creating our database, we create a parameter group for our cluster and modify the binlog parameter: 
binlog_format :  Row 
binlog_checksum :  None
binlog_cache_size : 32768

![binlog](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/ac9cc517-152e-43ac-b57d-5261a68a5660)

![Parameter group of RDS](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/c332b97d-7311-43f8-b082-e6b8eaa79e05)

## Creating the Aurora MySQL database 
While creating ur database, make sure you are : 
- [ ] Retainning ur user name and password
- [ ] Connectivity: set up a connexion for EC2 instance 
- [ ] Retainning the subnet group setting
- [ ] Choosing the **default security group**
- [ ] Port 3306
- [ ] Selecting the DB cluster group we created before

![Aurora MySQL database](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/d4715e9d-2378-4905-a3dd-f0f186f95ff3)

# 6-Creating Users table 
Create table users with this command: 
mysql -h "endpoint" -u admin -p product_platform < commands.sql
then connect to your database and show tables;

# 7-Create a Datastream using Amazon Kinesis 
![Kinesis Datastream ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/e8f1e64d-7a26-416d-b3d8-278f40a42b91)

# 8-Create IAM role that will be used by AWS DMS to interact with Kinesis
First we should create  a **new policy** for the Kinesis Service with : 
Action: Read: DescribeStream 
	      Write: PutRecords PutRecord
Resources: specify a stream resource ARN
![policy actions for IAM Role for DMS](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/079bc08f-9ecf-4cc5-8209-54455f1e8622)

**then attach your policy to your IAM Role**
![DMS Role](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/a65518e4-590b-433d-9de6-918349b650d0)

# 9-Amazon DMS

In this service we will perform 3 steps : 
## Create a replication instance which will be used to run our migration tasks 
make sure to select the VPC our instance will run on, and let the other configuration as default.
![replication instance](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/96b37cd8-8c04-4bce-b2d3-73ff6a6a36b7)

## Create the endpoints that will allow AWS DMS to read from and write to our database 
### First: source endpoint (AuroraMySQL Writer)
### Second: target endpoint (Amazon Kinesis)
![endpoints for DMS ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/8b4f2621-e592-423a-989a-00a0ea86dbc5)

## Create Database migration tasks
While creating the DMS task, we gonna specify the schema : 
![DMS migration task config](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/1c65e5a4-3970-4975-8c4b-c4703bafbc36)
Exceute the task : 
![DMS task execution](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/8d35eb44-7c02-418c-9be7-c142442cae15)
the load is complete in almost 4min !

# 10-Read from Kinesis Data Stream 
 Execute this file to read the first 10 records from kinesis : read_kinesis_first_10_records.py .
 Then update our database by changing the userid : execute this file aurora_update_single_row.py 
 Next, we can perform a continuous update on multiple rows and see the changes made to our database : execute this file on a new EC2 session read_kinesis_update.py, use one session for updating changes and other one for seeing those changes.
![read first 10 records](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/b96b28bb-57df-40aa-a119-afbc42f0d33b)
![update a single row](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/d473e045-1357-4761-8560-8aca930059cf)
![read updates](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/0505acea-61e4-486f-9ff8-a59ebd5adc0e)

 # 11-Creating Transformation Job on AWS Glue from the Visual ETL 
 As I mentioned below, our dataset contain some sensitive data. In order to keep this data private during the CDC we gonna run a job before the data arrives on S3 bucket.
 **Don't forget to create IAM role to read from kinesis data stream and write to S3 for the AWS Glue Service ! **
 
 - [ ] Source : Kinesis Data Stream 
 - [ ] Transform : 
   Flatten : to deal with our JSON format, we gonna turn it into a flat, tabular format to facilitate the storage after.
   Detect Sensitive Data : Detect PII, It will detect the phone number and email adress then replace it with ##### string.
- [ ] Target : Amazon S3
![glue job from visual etl](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/f53f8665-6942-4610-87c2-1a19c3dc1a4f)

We can have access to the script generated by AWS Glue to exectue this ETL :
![transform script generated](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/1a9b3815-9698-4010-8033-42d4c1aa8737)

**Run your job and let's meet on Athena ! **

# 12-Amazon Athena 
Simple Query to see our first 10 rows : 
SELECT * FROM "AwsDataCatalog"."default"."users" limit 10;
![transformed data at athena](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/7ff2e880-6d61-4446-802f-0adff52e3a86)









