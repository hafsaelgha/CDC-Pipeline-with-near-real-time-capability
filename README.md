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
![architecture](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/9d722b0b-7016-465f-80fe-5a1c42888bd2)

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
![EC2 required installation](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/ecf769d8-5bc3-4b4b-b786-1c446b3f826f)
![EC2 required installation 2 ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/639e2a48-6521-4cbe-a765-ba69ee3292cd)


# 5-Create Amamzon Aurora MySQL compatible database from RDS

## Parameter Group 
Fisrt, **The binlog** is a log file in MySQL that records all changes **(inserts, updates, deletes)** made to the database. It acts as a chronological record of every data modification operation.
Before creating our database, we create a parameter group for our cluster and modify the binlog parameter: 
binlog_format :  Row 
binlog_checksum :  None
binlog_cache_size : 32768

![binlog](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/2edd9cd1-0d41-47c0-b329-5cbef703aec8)

![Parameter group of RDS](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/683725bd-7ffb-4915-99db-2d0c2ec34668)



## Creating the Aurora MySQL database 
While creating ur database, make sure you are : 
- [ ] Retainning ur user name and password
- [ ] Connectivity: set up a connexion for EC2 instance 
- [ ] Retainning the subnet group setting
- [ ] Choosing the **default security group**
- [ ] Port 3306
- [ ] Selecting the DB cluster group we created before

![Aurora MySQL database](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/b7ea52c6-37e5-4486-98c5-474ef54764be)


# 6-Creating Users table 
Create table users with this command: 
mysql -h "endpoint" -u admin -p product_platform < commands.sql
then connect to your database and show tables;

# 7-Create a Datastream using Amazon Kinesis 
![Kinesis Datastream ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/60bf0750-472b-4b37-bc0a-1991bf4b947e)



# 8-Create IAM role that will be used by AWS DMS to interact with Kinesis
First we should create  a **new policy** for the Kinesis Service with : 
Action: Read: DescribeStream 
	      Write: PutRecords PutRecord
Resources: specify a stream resource ARN
![policy actions for IAM Role for DMS](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/6ff398d2-6d8f-42a3-9d89-29ca082b5bf7)


**then attach your policy to your IAM Role**
![DMS Role](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/291493a6-2d28-4252-b508-b4e152481bc7)


# 9-Amazon DMS

In this service we will perform 3 steps : 
## Create a replication instance which will be used to run our migration tasks 
make sure to select the VPC our instance will run on, and let the other configuration as default.
![replication instance](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/9727de72-6469-46fd-b7fe-04e55f938357)


## Create the endpoints that will allow AWS DMS to read from and write to our database 
### First: source endpoint (AuroraMySQL Writer)
### Second: target endpoint (Amazon Kinesis)
![endpoints for DMS ](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/a38f00ca-ab35-456e-b330-732251d38f62)


## Create Database migration tasks
While creating the DMS task, we gonna specify the schema : 
![DMS migration task config](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/51c9c8e6-a86a-48e0-b173-5ae6ec632e60)

Exceute the task : 
![DMS task execution](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/55107704-e471-4937-804d-f66caa5b6dab)

the load is complete in almost 4min !

# 10-Read from Kinesis Data Stream 
 Execute this file to read the first 10 records from kinesis : read_kinesis_first_10_records.py .
 Then update our database by changing the userid : execute this file aurora_update_single_row.py 
 Next, we can perform a continuous update on multiple rows and see the changes made to our database : execute this file on a new EC2 session read_kinesis_update.py, use one session for updating changes and other one for seeing those changes.

![read first 10 records](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/456aa9e5-c0f5-4892-8d20-b024b0700bf5)
![update a single row](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/9b01d8a6-49a0-4677-a064-ec1d84ef5975)
![read updates](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/47862084-86e6-4b9d-af04-7763925d22e5)


 # 11-Creating Transformation Job on AWS Glue from the Visual ETL 
 As I mentioned below, our dataset contain some sensitive data. In order to keep this data private during the CDC we gonna run a job before the data arrives on S3 bucket.
 
 **Don't forget to create IAM role to read from kinesis data stream and write to S3 for the AWS Glue Service !**
 
 - [ ] Source : Kinesis Data Stream 
 - [ ] Transform : 
   Flatten : to deal with our JSON format, we gonna turn it into a flat, tabular format to facilitate the storage after.
   Detect Sensitive Data : Detect PII, It will detect the phone number and email adress then replace it with "#####" string.
- [ ] Target : Amazon S3
![glue job from visual etl](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/6ed5d5c8-f761-4fc9-97c7-9c45b4de4ec7)


We can have access to the script generated by AWS Glue to exectue this ETL :
![transform script generated](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/528a4653-48e5-46bd-9f05-46d78043633a)


**Run your job and let's meet on Athena ! **

# 12-Amazon Athena 
Simple Query to see our first 10 rows : 
SELECT * FROM "AwsDataCatalog"."default"."users" limit 10;
![transformed data at athena](https://github.com/hafsaelgha/CDC-Pipeline-with-near-real-time-capability/assets/99973359/decf72c2-8b86-4b73-a5d4-6a684a0ceae6)









