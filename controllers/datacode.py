import sqlite3
import csv
from .crproject import dictionary

def info(name):
    parts = name.split()  # Split the name into parts
    initials = [part[0].upper() for part in parts if not part.startswith("Dr.")]  # Extract initials, ignoring "Dr."
    return "".join(initials)

def create_tables():
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    days=['MON','TUE','WED','THU','FRI']
    for day in days:
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS {day} (
                                staff_code CHAR(10) PRIMARY KEY,
                                subject TEXT,
                                name TEXT,
                                hour1 CHAR(5) NULL,
                                hour2 CHAR(5) NULL,
                                hour3 CHAR(5) NULL,
                                hour4 CHAR(5) NULL,
                                hour5 CHAR(5) NULL,
                                hour6 CHAR(5) NULL,
                                hour7 CHAR(5) NULL
                            )'''
        cursor.execute(create_table_sql)
        with open ("controllers/staff.csv","r",newline='\r\n') as f:
            creader=csv.reader(f)
            next(creader,None)
            for rec in creader:
                acode=info(rec[1])
                cursor.execute(f'''INSERT INTO {day} (staff_code,subject, name) VALUES (?,?,?)''',(acode,rec[2],rec[1]))

    # Commit changes and close connection
    conn.commit()
    conn.close()

def delete_tables():
    conn = sqlite3.connect("newdatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        #print(f"Dropped table: {table_name}")
    conn.commit()
    conn.close()

    

