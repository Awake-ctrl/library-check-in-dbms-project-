import sys
import csv
import psycopg2
import os
from PIL import Image

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

def get_photo(photo_path, membership_id, extension):
    dict = [".jpg", ".jpeg", ".JPG", ".png", ".PNG"]
    for ext in dict:
        path = os.path.join(photo_path, f"{membership_id}{ext}")
        if os.path.exists(path):
            try:
                with Image.open(path) as img:
                    img.verify()
                return path
            except (IOError, SyntaxError):
                pass
    return None

def process_csv(conn, filename, photo_path):
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            cursor = conn.cursor()

            for row in reader:
                membership_id = row[0]
                name = row[1]
                category = row[2]
                sex = row[3]
                extension = "\\"
                photo = get_photo(photo_path, membership_id, extension)

                if "pdf" in membership_id.lower():
                    print(f"Ignoring record with membership ID: {membership_id}")
                    continue

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
                        department = "UNKNOWN"

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

                if department and program:
                    sql = """INSERT INTO student (id, name, department, program, photo, valid_year)
                             VALUES (%s, %s, %s, %s, %s, %s)
                             ON CONFLICT (id) DO UPDATE
                             SET name = EXCLUDED.name,
                                 department = EXCLUDED.department,
                                 program = EXCLUDED.program,
                                 photo = EXCLUDED.photo,
                                 valid_year = EXCLUDED.valid_year"""
                    cursor.execute(sql, (membership_id, name, department, program, photo if photo else None, None))
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python insertdata.py <csv_file_path> <photo_folder_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    photo_folder_path = sys.argv[2]

    conn = connect_to_postgres()
    if conn:
        process_csv(conn, csv_file_path, photo_folder_path)

