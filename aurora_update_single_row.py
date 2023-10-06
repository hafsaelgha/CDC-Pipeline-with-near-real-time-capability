import mysql.connector
import random

#MySQL database configuration
db_config = {
    "host": "aurora-mysql-database-1.cluster-cvpckpe23lll.us-east-1.rds.amazonaws.com", #endpoint_writer
    "user": "admin",
    "password": "admin123",
    "database": "aurora-mysql-database-1"
}

#Establish a connection to the Aurora MySQL database
conn = mysql.connector.connect(**db_config)

#Create a cursor to execute SQL queries
cursor = conn.cursor()

try:
    current_id = random.randint(1, 277)
    new_id = random.randint(1, 277)

    #SQL Query to update the row and execute it
    update_query = f"UPDATE your_table SET ID = {new_id} WHERE ID = {current_id}"
    cursor.execute(update_query)

    #Commit changes
    conn.commit()

    #Print results
    print(f"ID {current_id} is updated to {new_id}")

except Exception as e:
    print(f"Erreur : {e}")

finally:
    cursor.close()
    conn.close()
