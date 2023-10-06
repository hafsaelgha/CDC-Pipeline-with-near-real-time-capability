import mysql.connector
import random
import time

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
    for _ in range(20):
        current_id = random.randint(1, 277)
        new_id = random.randint(1, 277)

        #Query to update the ID of the specific row and execute it 
        update_query = f"UPDATE your_table SET ID = {new_id} WHERE ID = {current_id}"
        cursor.execute(update_query)

        #Commit the changes to the database
        conn.commit()

        #Print the result of the update
        print(f"ID {current_id} updated with the new value {new_id}")

        #Introduce a 2-second delay before the next update
        time.sleep(2)

except Exception as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()
