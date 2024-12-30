import sqlite3
from tt_writer import tt_d,spl
import secrets
from normal import someother
from simple import errorcnt,subject_finder,least_occurred_code
from final_writer import finalwriting,central_allocation
d=tt_d()
def update(day,hrs,code,roomno):
    conn = sqlite3.connect('yourdatabase.db')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE {roomno} SET {hrs}=? WHERE day=? ''',(code,day))
    conn.commit()
    conn.close()
def allocate(day,hrs,code,roomno):
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE  {day} SET {hrs}= ? WHERE staff_code=?''',(roomno,code))
    conn.commit()
    conn.close()
def checking(avi,inst,num,day,roomno):
    slots=inst.slots
    working_days=['MON','TUE','WED','THU','FRI']
    slot=slots[working_days.index(day)]
    for i in avi:
        ace=[part[0] for part in slots]
        i=i[0]
        if(num==0):
            if(ace.count(slot[0])>1):
                if(i in[inst.staff[0],inst.staff[1],inst.staff[2]]):
                    slot[num]=i
                    i=d[roomno].subject[i]+'/'+i
                    allocate(day,'hour'+str(num+1),i,roomno)
                    update(day,'hour'+str(num+1),i,roomno)
                    return i
                else:
                    continue
            else:
                #print("Hi")
                print("CALL FOR",slot[num],roomno)
                someother(d,roomno,slot[num],'CSE')
                break  

        else:
            i=least_occurred_code(d[roomno].slots,avi)
            if(slot.count(i)==2):
                continue
            else:
                slot[num]=i
                i=d[roomno].subject[i]+'/'+i
                allocate(day,'hour'+str(num+1),i,roomno)
                update(day,'hour'+str(num+1),i,roomno)
                return i

def free(hr):
    conn = sqlite3.connect('newdatabase.db')
    cursor = conn.cursor()
    k=d[hr[0]]
    cursor.execute(f'''
                    SELECT staff_code 
                    FROM {hr[2]} 
                    WHERE {hr[3]} IS NULL 
                    AND staff_code IN (?,?,?,?,?)
                    ''', k.staff)

    avilable=cursor.fetchall()
    conn.close()
    return avilable
def clash_check(hr):
    if(errorcnt(hr,spl)):
        print("call for",hr[1],hr[0])
        k=subject_finder(hr[1],d[hr[0]].staff)
        someother(d,hr[0],hr[1],k)
        dummy.append(hr[:2])
        print(dummy)
    else:
        avi=free(hr)
        #print(avi)
        i=checking(avi,d[hr[0]],int(hr[3][4])-1,hr[2],hr[0])

print(spl)
dummy=[]
for i in spl:
    if(i[:2] not in dummy):
        clash_check(i)

finalwriting(d)
central_allocation(d)


    
        
