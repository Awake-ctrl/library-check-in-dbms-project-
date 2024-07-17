# 

import csv
import psycopg2
import os
from PIL import Image
# Function to establish connection to PostgreSQL
def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL successfully")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
def get_photo(photo_path,membership_id,extension):
    dict=[".jpg",".jpeg",".JPG",".png",".PNG"]
    # print(len(dict))
    for index in range(len(dict)):
        # print(index)
        # print(type)"D:\albert sunny project\photos\142201003.jpeg"
        path=photo_path+extension+str(membership_id)+dict[index]
# The `print(path)` statement in the code is used to display the full path of the image file
# being checked in the `get_photo` function. This helps in debugging and understanding which
# image file path is being processed at that point in the code.
#  print(path)
        if os.path.exists(photo_path):
            try:
                with Image.open(path) as img:
                    img.verify()  # Verify if it's a valid image
                return path
            except (IOError, SyntaxError) as e:
                pass
    return None
# Function to read CSV file and process data
def process_csv(conn, filename,photo_path):
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            cursor = conn.cursor()
           

            for row in reader:
                membership_id = row[0]
                name = row[1]
                category = row[2]
                sex = row[3]
                # photo=photo_path+f"\{membership_id}"+".jpg"
                # print(photo)
                extension=f"\\"
                photo=get_photo(photo_path,membership_id,extension)

                # Check if membership_id contains "pdf", skip processing if it does
                if "pdf" in membership_id.lower():
                    print(f"Ignoring record with membership ID: {membership_id}")
                    continue

                # Determine program and department based on category and membership_id
                program = ""
                department = ""

                if category == "RS":
                    program = "Research Scholar"
                    if membership_id.startswith("17"):
                        department = "Biological Science and Engineering"
                    elif membership_id.startswith("20"):
                        department = "Chemistry"
                    elif membership_id.startswith("10"):
                        department = "Civil Engineering"
                    elif membership_id.startswith("11"):
                        department = "Computer Science and Engineering"
                    elif membership_id.startswith("14"):
                        department = "Data Science"
                    elif membership_id.startswith("12"):
                        department = "Electrical Engineering"
                    elif membership_id.startswith("16"):
                        department = "ESSENCE"
                    elif membership_id.startswith("23"):
                        department = "Humanities and Social Sciences"
                    elif membership_id.startswith("21"):
                        department = "Mathematics"
                    elif membership_id.startswith("13"):
                        department = "Mechanical Engineering"
                    elif membership_id.startswith("22"):
                        department = "Physics"
                    else:
                        department="UNKNOWN"

                elif category == "ST":
                    program = "UG"
                    if membership_id.startswith("11"):
                        department = "Computer Science and Engineering"
                    elif membership_id.startswith("12"):
                        department = "Electrical Engineering"
                    elif membership_id.startswith("10"):
                        department = "Civil Engineering"
                    elif membership_id.startswith("13"):
                        department = "Mechanical Engineering"
                    elif membership_id.startswith("14"):
                        department = "Data Science and Engineering"

                elif category == "ST-PG":
                    program = "PG"
                    if membership_id.startswith("10"):
                        department = "Geotechnical Engineering"
                    elif membership_id.startswith("11"):
                        department = "Computing and Mathematics"
                    elif membership_id.startswith("12"):
                        department = "Power Electronics and Power Systems"
                    elif membership_id.startswith("13"):
                        department = "Manufacturing and Materials Engineering"
                    elif membership_id.startswith("14"):
                        department = "Data Science and Engineering"
                    elif membership_id.startswith("15"):
                        department = "System-on-Chip Design"
                    elif membership_id.startswith("20"):
                        department = "Chemistry"
                    elif membership_id.startswith("21"):
                        department = "Mathematics"
                    elif membership_id.startswith("22"):
                        department = "Physics"

                # Insert or update record into PostgreSQL table
                if department and program:  # Ensure both program and department are determined
                    sql = """INSERT INTO student (id, name, department, program, photo, valid_year)
                             VALUES (%s, %s, %s, %s, %s, %s)
                             ON CONFLICT (id) DO UPDATE
                             SET name = EXCLUDED.name,
                                 department = EXCLUDED.department,
                                 program = EXCLUDED.program,
                                 Photo = EXCLUDED.Photo,
                                 valid_year = EXCLUDED.valid_year"""
                    cursor.execute(sql, (membership_id, name, department, program,photo if photo else None, None))   #psycopg2.Binary(photo)
                    if photo:
                        print(photo)
                    conn.commit()
                else:
                    print(f"Skipping record with incomplete data: {membership_id}")

            print("Data insertion into PostgreSQL successful")
            cursor.close()

    except psycopg2.Error as e:
        print(f"Error executing SQL: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("PostgreSQL connection is closed")

# Main execution starts here
if __name__ == "__main__":
    conn = connect_to_postgres()
    #input a=file
    file="D:\\albert sunny project\photos"
    print(file)
    # photo_path="D:\albert sunny project\photos"
    if conn:
        process_csv(conn, 'student.csv',file)
