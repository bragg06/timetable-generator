import sqlite3
from .simple import union, change
from .tt_writer import tt_work
from .staff_writer import staff_work
import random
def someother(d,roomno,code,sub):
    totfree=[]
    #print('Hi')
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    for day in ['MON','TUE','WED','THU','FRI']:
        cursor.execute(f'''SELECT staff_code FROM {day} WHERE subject= ?
                    AND hour1 IS NULL AND hour2 IS NULL AND hour3 IS NULL 
                    AND hour4 IS NULL AND hour5 IS NULL AND hour6 IS NULL AND hour7 IS NULL''',(sub,))
        totfree.append(cursor.fetchall())
    conn.close()
    #print(totfree)
    u=union(totfree)[0]
    print(u)
    change(d[roomno].slots,code,u,d[roomno].staff,d[roomno].subject,d[roomno].sub_name)
    staff_work(d)
    tt_work(d)

def info(name):
    parts = name.split()  # Split the name into parts
    initials = [part[0].upper() for part in parts if not part.startswith("Dr.")]  # Extract initials, ignoring "Dr."
    return "".join(initials)

def teacher_name(staffs):
    staffs=tuple(staffs)
    conn=sqlite3.connect('newdatabase.db')
    cursor=conn.cursor()
    placeholders = ', '.join('?' for _ in staffs)
    # Construct the SQL query
    query = f'SELECT name FROM MON WHERE staff_code IN ({placeholders})'
    # Execute the query with the staff codes as parameters
    cursor.execute(query, staffs)
    names=cursor.fetchall()
    names=(part[0] for part in names)
    conn.close()
    dd={}
    for i in names:
        k=info(i)
        dd[k]=i

    return dd

def free_morn(i,day):
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT staff_code FROM {day} WHERE subject= 'CSE'
                    AND {'hour'+str(i+1)} IS NULL AND {'hour'+str(i+2)} IS NULL 
                    AND {'hour'+str(i+3)} IS NULL''')
    free_staff=[part[0] for part in cursor.fetchall()]
    conn.close()
    return (free_staff)

def free3 (slots):
    day=['MON','TUE','WED','THU','FRI']
    dummy=[]
    labs={}
    for sch in slots:
        if('Lab1' in sch):
            index=sch.index('Lab1')
            labstaff=free_morn(index,day[slots.index(sch)])
            l=random.choice(labstaff)
            l=(l,day[slots.index(sch)])
            while l in dummy: l=random.choice(labstaff)
            dummy.append(l)
            labs['Lab1']=l[0]

        if('Lab2' in sch):
            index=sch.index('Lab2')
            labstaff=free_morn(index,day[slots.index(sch)])
            l=random.choice(labstaff)
            l=(l,day[slots.index(sch)])
            while l in dummy: l=random.choice(labstaff)
            dummy.append(l)
            labs['Lab2']=l[0]
        
        if('Lab3' in sch):
            index=sch.index('Lab3')
            labstaff=free_morn(index,day[slots.index(sch)])
            l=random.choice(labstaff)
            l=(l,day[slots.index(sch)])
            while l in dummy: l=random.choice(labstaff)
            dummy.append(l)
            labs['Lab3']=l[0]
    return labs
        
        



    
