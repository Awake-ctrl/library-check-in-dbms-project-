import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'library_dbms',
    'user': 'postgres',
    'password': 'S@i*iran2004',
    'host': 'localhost',
    'port': '5432'
}

# SQL statement to create the students table with a photo column
create_table_query = """
CREATE TABLE IF NOT EXISTS student (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    photo BYTEA
);
"""

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    # Execute the SQL statement
    cursor.execute(create_table_query)
    conn.commit()
    
    print("Table created successfully")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    if conn:
        cursor.close()
        conn.close()
