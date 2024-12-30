import sqlite3
from .datacode import create_tables , delete_tables
from .lab_writer import lab_d
spl=[]
d=lab_d()
def staff_work(d):
    delete_tables()          
    create_tables()
    for ele in d:
        element=d[ele]
        conn = sqlite3.connect("newdatabase.db")
        cursor = conn.cursor()
        days=['MON','TUE','WED','THU','FRI']
        for i,j in zip(days,element.slots):
            count=0
            for k in j:
                hrs='hour'+str(count+1)
                if(k in element.staff):
                    cursor.execute(f'''SELECT {hrs},staff_code FROM {i} WHERE staff_code=?''',(k,))
                    obj=cursor.fetchall()[0]
                    if(None not in obj):
                        spl.append(obj+(i,hrs))
                    cursor.execute(f'''UPDATE {i} SET {hrs}=? WHERE staff_code=?''', (ele, k))
                    #print(ele,k,i,hrs)
                count+=1
        conn.commit()
        conn.close()
def stadff_d():
    staff_work(d)
    return d