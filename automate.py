import random
from datetime import date
# INSERT TICKET 
# print(date.today().strftime('%d/%m/%Y'))

t_id = 25

title = 'Runtime expensive'
desc = 'system 3 has wrong data file'
user_create = 'demo_user'
user_assigned = 'demo_dev'
d1='2/9/2020'
d2='6/9/2020'
d3='8/9/2020'
d4='5/10/2020'
p_id = 5
user_id = ['19','20','20']

submitter= user_create+'@gmail.com'
status= 'open'
arr_p = ["High","Low","Medium"]
priority= arr_p[random.randint(0,2)]
type = 'bug'
start = d1
end = d4
tick = ''
# insert into ticket values('1', 'title', 'desc', userid,'submitter',p_id, prioirit, status, type, creaetedate, N/A)"
tick = "insert into ticket values("+ str(t_id) +", '"+title +"', '"+desc+"','"+user_id[1]+"' ,'"+submitter+"',"+ str(p_id)+", '"+ priority+"', '"+status+"', '"+type+"', '"+ start +"', '"+ end +"');"
print(tick)

#insert into ticket_history values(id,t_id, user_id, status, date, priority)

arr_status =['open','open','in-progress', 'closed']
arr_date = [d1,d2,d3,d4]
print()
user__id = ['0',user_id[1],user_id[1],user_id[1],user_id[1]]
for i in range(1 , 5):
    tick_history = "insert into ticket_history values("+str(4*(t_id-1)+i)+","+str(t_id)+", '"+user__id[i-1]+"', '"+arr_status[i-1]+"', '"+arr_date[i-1]+"','"+ priority+"');"
    print(tick_history)

#insert into comment values(c_id, t_id, users_id, "date", "comment")
c1 = user_assigned+" assigned to this ticket"
c2 = 'status changed to in-progess'
c3 = 'Status changed to closed'
arr_c = [c1,c2,c3]
arr_date=[d2,d3,d4]
print()
for i in range(1, 4):
    comment = "insert into comment values("+str(3*(t_id-1)+i)+","+ str(t_id)+","+ user_id[i-1] +",'"+ arr_date[i-1] +"', '"+arr_c[i-1]+"');"
    print(comment)
