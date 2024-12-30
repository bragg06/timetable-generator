import sqlite3
from .staff_writer import stadff_d , spl
from .simple import super_subjects
d=stadff_d()
def tt_work(d):
    working_day=['MON','TUE','WED','THU','FRI']
    conn = sqlite3.connect('yourdatabase.db')
    cursor = conn.cursor()
    for room in d:
        lst=super_subjects(d[room].slots,d[room].subject)
        for day in lst:
            #print(day)
            wday=working_day[lst.index(day)]
            cursor.execute(f'''UPDATE {room} SET hour1= ?,hour2=?,hour3=?,hour4=?,hour5=?,hour6=?,hour7=?
                            WHERE day= ?''',(day[0],day[1],day[2],day[3],day[4],day[5],day[6],wday))
    conn.commit()
    conn.close()  

def tt_d():
    tt_work(d)
    return d

