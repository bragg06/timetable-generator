import random
import secrets
from collections import Counter
def checker(l,cse_staff):
        if(l[0] in cse_staff):
            return 1
        else:
            return 0
def swap(l):
    if('ICELL'in l): 
        k=l.index('ICELL')
        l[k],l[6]=l[6],l[k]
    elif('Library'in l):
        k=l.index('Library')
        l[k],l[6]=l[6],l[k]
def generate_unique_random(existing_numbers, min_num, max_num):
        while True:
            num = random.randint(min_num, max_num) 
            if num not in existing_numbers: 
                existing_numbers.append(num)  
                return num  
def unique(tt_slots,cse_staff):
    slot=[slots[0] for slots in tt_slots]
    if(len(list(set(slot)))==1):
        for i in tt_slots[0]:
            if(i in cse_staff and i not in slot):
                s=tt_slots[0].index(i)
                tt_slots[0][0],tt_slots[0][s]=tt_slots[0][s],tt_slots[0][0]
                slot.append(i)
                break
        for i in tt_slots[1]:
            if(i in cse_staff and i not in slot):
                s=tt_slots[1].index(i)
                tt_slots[1][0],tt_slots[1][s]=tt_slots[1][s],tt_slots[1][0]
                break
        return tt_slots
    elif(len(list(set(slot)))==2):
        for i in tt_slots[0]:
            if(i in cse_staff and i not in slot):
                s=(tt_slots[0].index(i))
                tt_slots[0][0],tt_slots[0][s]=tt_slots[0][s],tt_slots[0][0]
                break
        return tt_slots
    else:
        return tt_slots
def union(l):
    dummy=[]
    for i in l[0]:
        if (i in l[1] and i in l[2] and i in l[3] and i in l[4]):
            dummy.append(i[0])

    return(dummy)    

def change(slots,old,new,staff,subject,subname):
    #print('Zz')
    for i in range (len(staff)):
        if(staff[i]==old):
            staff[i]=new
    
    val=subject.pop(old)
    subject[new]=val
    val=subname.pop(old)
    subname[new]=val

    for i in range (5):
        for j in range (7):
            if(slots[i][j]==old):
                slots[i][j]=new

def crypto_shuffle(lst):
    shuffled_list = lst[:]  # Create a copy to avoid modifying the original list
    for i in range(len(shuffled_list) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        shuffled_list[i], shuffled_list[j] = shuffled_list[j], shuffled_list[i]
    return shuffled_list

def remove_duplicates(spl):
    unique_pairs = set()  # Set to store unique pairs
    result = []  # List to store the filtered elements
    for item in spl:
        pair = (item[0], item[1])  # Extract the first two elements as a pair
        if pair not in unique_pairs:
            unique_pairs.add(pair)
            result.append(item)
    return result


def errorcnt(i,spl):
    count=0
    for x in spl:
        if x[0] == i[0] and x[1] == i[1] and x != i:
            count+=1
    if(count>2):
        remove_duplicates(spl)
        return 1
    else:
        return 0
    
def subject_finder(code,staff):
    for i in staff:
        if(code==i):
            if(staff.index(code) in (1,2,0)):
                return 'CSE'
            if(staff.index(code)==3):
                return 'MATH'
            if(staff.index(code)==4):
                return 'PHY'
 
def least_occurred_code(slots, available):
    # Flatten the list of lists into a single list
    all_codes = [code for sublist in slots for code in sublist]

    # Count occurrences of each code
    code_counts = {}
    for code in all_codes:
        if code in code_counts:
            code_counts[code] += 1
        else:
            code_counts[code] = 1

    # Find the least occurred code among available codes
    least_occurred = None
    min_count = float('inf')  # Initialize min_count to positive infinity
    for code_tuple in available:
        code = code_tuple[0]  # Extract the code from the tuple
        if code in code_counts and code_counts[code] < min_count:
            least_occurred = code
            min_count = code_counts[code]

    return least_occurred

def super_subjects(slots,subs):
    lst=[[],[],[],[],[]]
    k=0
    for i in slots:
        for j in i:
            if(j not in ('P&T','Tamil','Library','ICELL','EVS')):
                lst[k].append(subs[j]+'/'+j)
            else:
                lst[k].append(j)
        k+=1
    return lst