import sqlite3
import random
import controllers.simple as simple
import controllers.imp_gui as imp_gui
from .basecode import creating_tables,deleting_tables
class tt:
    def __init__(self,roomno):
        self.roomno=roomno
        self.staff=[]
        self.assign()
        self.course()
        self.combinations()
    def assign(self):
        conn = sqlite3.connect("controllers/newdatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT staff_code,subject FROM MON WHERE subject IS ?",('CSE',)) 
        crows = cursor.fetchall()
        print("length",len(crows))
        dummy=[]
        for i in range (1,4):
            k=simple.generate_unique_random(dummy,1,len(crows))-1
            self.staff.append(crows[k][0])
        cursor.execute("SELECT staff_code,subject FROM MON WHERE subject IS ?",('MATH',)) 
        mrows = cursor.fetchall()
        self.staff.append(mrows[random.randint(0,len(mrows)-1)][0])
        cursor.execute("SELECT staff_code,subject FROM MON WHERE subject IS ?",('PHY',)) 
        prows = cursor.fetchall()
        self.staff.append(prows[random.randint(0,len(prows)-1)][0])
        #print(self.staff)
        conn.close()
    def course(self):
        entire=self.staff+['Lab1','Lab2','Lab3']
        sub,subname=imp_gui.getsubjects(self.roomno,entire)
        self.sub_name=dict(zip(entire,subname))
        self.subject=dict(zip(entire,sub))
        print(self.subject)
    def shuffle(self,l):
        random.shuffle(l)
        if(l not in self.slots and simple.checker(l,[self.staff[0],self.staff[1],self.staff[2]])):
                 simple.swap(l)
                 return self.slots.append(l)
        else:
            self.shuffle(l)  
    def day2day(self,l,dummy):
        extras1=[self.staff[0],self.staff[1],self.staff[2]]
        extras2=['Library','ICELL','Tamil',self.staff[3],'EVS']
        i = simple.generate_unique_random(dummy, 0, 4)
        l.append(random.choice(extras1))
        l.append(extras2[i])
    def combinations(self):
        self.slots=[]
        dummy=[]
        for i in range (5):
            l=self.staff[:]
            self.day2day(l,dummy)
            self.shuffle(l)
        self.slots=simple.unique(self.slots,[self.staff[0],self.staff[1],self.staff[2]])
        #print(self.slots)


d={}
classroom=imp_gui.getrooms() #frontend input module variable
deleting_tables("yourdatabase.db")
creating_tables(classroom)
for i in classroom:
    d[i]=tt(i)

def dictionary():
    return d