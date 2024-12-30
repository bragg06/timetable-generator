from .crproject import dictionary
from .simple import generate_unique_random 
d=dictionary()
for i in d:
    i=d[i]
    dummy=[]
    labcount=1
    while(labcount<5):
        n=generate_unique_random(dummy,0,4)
        day=i.slots[n]
        if(day[6] in ('ICELL','Library')):
            if(i.staff[3] in (day[1],day[2],day[3])):
                k=day.index(i.staff[3])
                day[4]=day[k]
                (day[1],day[2],day[3])=('Lab'+str(labcount),)*3
            else:
                (day[1],day[2],day[3])=('Lab'+str(labcount),)*3
        else:
            if('EVS' in (day[1],day[2],day[3])):
                j=day.index('EVS')
                if(i.staff[3] in (day[4],day[5],day[6])):
                    k=day.index(i.staff[3])
                    if(j==1):
                        day[2]=day[k]
                    else:
                        day[j-1]=day[k]
                    (day[4],day[5],day[6])=('Lab'+str(labcount),)*3
                else:
                    (day[4],day[5],day[6])=('Lab'+str(labcount),)*3
            elif('Tamil'in (day[1],day[2],day[3])):
                j=day.index('Tamil')
                if(i.staff[3] in (day[4],day[5],day[6])):
                    k=day.index(i.staff[3])
                    if(j==1):
                        day[2]=day[k]
                    else:
                        day[j-1]=day[k]
                    (day[4],day[5],day[6])=('Lab'+str(labcount),)*3
                else:
                    (day[4],day[5],day[6])=('Lab'+str(labcount),)*3
            else:
                if(i.staff[3] in (day[4],day[5],day[6])):
                    k=day.index(i.staff[3])
                    day[4]=day[k]
                    (day[1],day[2],day[3])=('Lab'+str(labcount),)*3
                else:
                    (day[1],day[2],day[3])=('Lab'+str(labcount),)*3
        labcount+=1
    
    x=str(4)
    for day in i.slots:
        if('Lab'+x in day):
            k=day.index('Lab'+x)
            day[k],day[k+1]='P&T','P&T'
            day[k+2]=i.staff[4]
            if(k==1):
                day[1],day[4]=day[4],day[1]
                day[2],day[5]=day[5],day[2]
            break
      
    #print(i.slots)
def lab_d():
    return d

