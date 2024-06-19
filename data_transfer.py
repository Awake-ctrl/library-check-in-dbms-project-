import pandas as pd
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'library_dbms',
    'user': 'postgres',
    'password': 'S@i*iran2004',
    'host': 'localhost',
    'port': '5432'
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)

# Read data from PostgreSQL table into a pandas DataFrame
df = pd.read_sql('SELECT * FROM students', conn)

# Write the DataFrame to an Excel file
df.to_excel("Book1.xlsx", index=False)

# Read data from an Excel file into a pandas DataFrame
df_from_excel = pd.read_excel('Book1.xlsx')

# Insert data from DataFrame into PostgreSQL table
for index, row in df_from_excel.iterrows():
    cursor = conn.cursor()
    # cursor.execute("""
    #     INSERT INTO your_table (column1, column2, column3)
    # #     VALUES (%s, %s, %s)
    # # """, (row['column1'], row['column2'], row['column3']))
    #     VALUES (%s, %s, %s, %s, %s)
    # """, (row['id'], row['name'], row['branch'], row['year'], row['ug_pg']))
    # conn.commit()
    cursor.execute("""
        INSERT INTO students (id, name, branch, year, ug_pg)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['id'], row['name'], row['branch'], row['year'], row['ug_pg']))
    conn.commit()

# Close the connection
conn.close()
