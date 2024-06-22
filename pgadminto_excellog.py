import psycopg2
import pandas as pd

# Database connection details
dbname = "library_dbms"
user = "postgres"
password = "S@i*iran2004"
host = "localhost"
port = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
cur = conn.cursor()

# Create the log table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS log (
        log_id SERIAL PRIMARY KEY,
        id VARCHAR(255),
        name VARCHAR(100),
        type VARCHAR(10),
        program VARCHAR(100),
        department VARCHAR(100),
        date DATE,
        library_name VARCHAR(255),
        checkin TIME,
        checkout TIME
    );
''')
conn.commit()

# Read the data from the server table (assuming the table is named `server_log`)
cur.execute('SELECT * FROM log;')
rows = cur.fetchall()

# Define column names for the dataframe
columns = ['log_id','id', 'name', 'type', 'program', 'department', 'date', 'checkin', 'checkout','library_name']

# Convert the data to a pandas DataFrame
log_df = pd.DataFrame(rows, columns=columns)

# Write the dataframe to an Excel file
log_df.to_excel('log_data.xlsx', index=False)

# Close the connection
cur.close()
conn.close()
