import sqlite3
def creating_tables(rooms):
    conn = sqlite3.connect('yourdatabase.db')
    cursor = conn.cursor()
    for room in rooms:
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS {room} (
                                    day CHAR(10) PRIMARY KEY,
                                    hour1 CHAR(10) NULL,
                                    hour2 CHAR(10) NULL,
                                    break1 CHAR(7) NULL,
                                    hour3 CHAR(10) NULL,
                                    hour4 CHAR(10) NULL,
                                    lunch char(7)  DEFAULT 'Lunch',
                                    hour5 CHAR(10) NULL,
                                    hour6 CHAR(10) NULL,
                                    break2 char(7) NULL,
                                    hour7 CHAR(10) NULL
                                )'''
        cursor.execute(create_table_sql)
        for day in ['MON','TUE','WED','THU','FRI']:
            cursor.execute(f'''INSERT INTO {room} (day) VALUES(?)''',(day,))
    conn.commit()
    conn.close()

def deleting_tables(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        #print(f"Dropped table: {table_name}")
    conn.commit()
    conn.close()

def creation(roomno):
    # Connect to SQLite database
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    create_table_query = f'''CREATE TABLE IF NOT EXISTS {roomno} (
                                staff_code char(7) PRIMARY KEY,
                                name char(30),
                                subject char(20),
                                subject_name char(50)
                                )'''
    cursor.execute(create_table_query)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def created(roomno):
    conn = sqlite3.connect("theirdatabase.db")
    cursor = conn.cursor()

    create_table_query = f'''CREATE TABLE IF NOT EXISTS {roomno} (
                                staff_code char(7) PRIMARY KEY,
                                name char(30),
                                lab_no char(5),
                                subject char(20),
                                subject_name char(50),
                                lab_name char(50)
                                )'''
    cursor.execute(create_table_query)

    # Commit changes and close connection
    conn.commit()
    conn.close()
