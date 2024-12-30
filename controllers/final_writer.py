import sqlite3
import random
from .normal import teacher_name,free3
from .basecode import deleting_tables,creation,created
labname=["Java Technology Lab","Windows Programming Lab","Graphics and Multimedia Lab","High Functionalitiy System Lab",
         "Ubuntu Software Lab","P G Lab 1","P G Lab 2","Artificial Inteligence and DBMS Lab","Distributed System Lab"]
def finalwriting(d):
    deleting_tables("mydatabase.db")
    deleting_tables("theirdatabase.db")
    #print(d)
    for x in d :
        #print(x)
        i=d[x]
        #print(i)
        dd=teacher_name(i.staff)
        creation(i.roomno)
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        for j in dd:
            cursor.execute(f'''INSERT INTO {i.roomno} VALUES(?,?,?,?)''',(j,dd[j],i.subject[j],i.sub_name[j]))
        conn.commit()        
        conn.close()
        created(i.roomno)
        conn = sqlite3.connect("theirdatabase.db")
        cursor = conn.cursor()
        ff=free3(i.slots)
        dd=teacher_name([ff[i] for i in ff])
        print(dd)
        print(ff)
        for (p, q), (r, s) in zip(dd.items(), ff.items()):
            cursor.execute(f'''INSERT INTO {i.roomno} VALUES (?,?,?,?,?,?) ''',(p,q,r,i.subject[r],i.sub_name[r],random.choice(labname)))
        conn.commit()        
        conn.close()

def allocate(day,hrs,code,roomno):
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE  {day} SET {hrs}= ? WHERE staff_code=?''',(roomno,code))
    conn.commit()
    conn.close()

def info(name):
    parts = name.split()  # Split the name into parts
    initials = [part[0].upper() for part in parts ]  # Extract initials, ignoring "Dr."
    return "".join(initials)

def central_allocation(d):
    actual_day=['MON','TUE','WED','THU','FRI']
    for i in d:
        i=d[i]
        conn=sqlite3.connect("theirdatabase.db")
        cursor=conn.cursor()
        for day in i.slots:
            if 'Lab1' in day:
                cursor.execute(f'''SELECT staff_code,lab_name FROM {i.roomno} WHERE lab_no='Lab1' ''')
                result=cursor.fetchone()
                if(result!= None):
                    val=list(result)
                    #print(val)
                    val[1]=info(val[1])
                    aday=i.slots.index(day)
                    allocate(actual_day[aday],'hour'+str(day.index('Lab1')+3),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab1')+1),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab1')+2),val[0],i.roomno+'/'+val[1])
            if 'Lab2' in day:
                cursor.execute(f'''SELECT staff_code,lab_name FROM {i.roomno} WHERE lab_no='Lab2' ''')
                result=cursor.fetchone()
                if(result != None):
                    val=list(result)
                    #print(val)
                    val[1]=info(val[1])
                    aday=i.slots.index(day)
                    allocate(actual_day[aday],'hour'+str(day.index('Lab2')+3),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab2')+1),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab2')+2),val[0],i.roomno+'/'+val[1])
            if 'Lab3' in day:
                cursor.execute(f'''SELECT staff_code,lab_name FROM {i.roomno} WHERE lab_no='Lab3' ''')
                result=cursor.fetchone()
                if(result!=None):
                    val=list(result)
                    #print(val)
                    val[1]=info(val[1])
                    aday=i.slots.index(day)
                    allocate(actual_day[aday],'hour'+str(day.index('Lab3')+3),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab3')+1),val[0],i.roomno+'/'+val[1])
                    allocate(actual_day[aday],'hour'+str(day.index('Lab3')+2),val[0],i.roomno+'/'+val[1])
        conn.close()
            
            






