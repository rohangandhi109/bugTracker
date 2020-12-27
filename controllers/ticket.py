####################### Header ######################################################
# Ticket Controller Includes                                                        #
# 1. Ticket form            /ticket-form            all can access                  #
# 2. Create ticket          /update-ticket          all can access                  #
# 3. Update ticket          /update-ticket          only admin can access           #
# 4. Ticket details         /ticket-details/{Id}    all can access                  #
# 6. change ticket status   /change-status          only dev can access             #
#####################################################################################

import sys
from datetime import date
from sqlalchemy import func
from flask import abort, request,render_template,redirect,url_for,session

from info import STATUS, PRIORITY
from app import app,db

from models.Ticket import Ticket
from models.Project import Project
from models.Users import Users
from models.Ticket_history import Ticket_history
from models.Map_users_proj import Map_users_proj
from models.Notification import Notification
from models.Comment import Comment

from controllers.notification import notify

################################### Genrate ticket form #####################################
# Endpoint generates a form for ticket                                                      #
# This can be also used for editing by setting the variable "edit"="true"                   #
# Renders -> ticket-form.html                                                               #
#############################################################################################

@app.route('/ticket-form', methods=['GET'])
def get_ticketForm():
    edit = request.args.get('edit')
    ticket = ""
    if edit == 'true':
        ticket = Ticket.query.get(request.args.get('ticketid'))

    project  = Project.query.all()
    project = [tick.format() for tick in project]
    data = {
        'edit':edit,
        'ticket':ticket.format(),
        'project':project,
        'priority':PRIORITY,
        'status':STATUS
    }
    return render_template('ticket-form.html',data=data)

################################### Create/Update ticket ########################################################
# End point is used to submit the form generate above.                                                          #
# Based on the varibale "action"-> new/update                                                                   #
# Creating a new ticket-> add an entry to ticket_history table and Insert into notification table               #
# Ticket status/priority updated -> add an entry to ticket_history table and Insert into notification table     #
# Renders -> list.html (Ticket table page, if action=new)                                                       #
# Renders -> ticket-detail.html (Ticket datails page, if action=update)                                         #
#################################################################################################################

@app.route('/update-ticket', methods=['POST'])
def create_ticket():
    
    #Get all values from the ticket form
    action = request.form.get('action')
    userInfo = session.get('userProfile')
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    users_id = 0
    submitter_email = userInfo['email']
    p_id = request.form.get('project')
    t_priority = request.form.get('t_priority','')
    t_type = request.form.get('t_type','')
    t_create_date = date.today().strftime("%d/%m/%Y")
    t_close_date = "N/A"

    ticketid =""
    new_id = db.session.query(func.max(Ticket.t_id))
    if new_id[0][0] == None:
        new_id=0

    # Genrate a new ticket
    if action=='new':
        ticket = Ticket(new_id[0][0]+1,t_title, t_desc, users_id, submitter_email, p_id, t_priority, 'open', t_type, t_create_date, t_close_date)
        try:
            ticket.insert()
        except:
            print(sys.exc_info())
            abort(500)
        
        ticketid = ticket.t_id

        # Add entry to history table 
        ticket_history = Ticket_history(ticket.t_id,users_id,'open',t_create_date,t_priority)
        try:
            ticket_history.insert()
        except:
            print(sys.exc_info())
            abort(500)

    # Authorize Admin


    # update ticket 
    if action=='update':
        ticketid = request.form.get('ticketid')
        ticket = Ticket.query.get(ticketid)
        t_date = t_create_date
        t_status = request.form.get('t_status')
        
        # status/priority changed add to ticket_history table
        if ticket.t_status != t_status or ticket.t_priority!= t_priority:
            ticket_history = Ticket_history(ticketid,ticket.users_id,t_status,t_date,t_priority)
            try:
                ticket_history.insert()
            except:
                print(sys.exc_info())
                abort(500)

        # status=closed, update the close_date
        if ticket.t_status!='closed' and t_status=='closed':
            ticket.t_close_date = t_create_date
        
        # update the ticket in the ticket table
        ticket.t_title = t_title
        ticket.t_desc = t_desc
        ticket.t_status = t_status
        ticket.t_priority = t_priority
        ticket.t_status = t_status
        ticket.t_type = t_type 
        
        ticket.update()
        ticketid = ticket.t_id
    
    # Fetch the people in the project
    project_user = Map_users_proj.query.with_entities(Map_users_proj.users_id).filter(Map_users_proj.p_id == p_id).all()

    # insert a notification record for each individual
    for p in project_user:
        notify = Notification(ticketid, p, type=action)
        try:
            notify.insert()
        except:
            print(sys.exc_info())
            abort(500)

    # Based on the role redirect to specific view ticket table end point
    if userInfo['role'] == 'dev':
        return redirect(url_for('get_project_tickets'))
    elif userInfo['role'] == 'user':
        return redirect(url_for('get_tickets'))
    elif action=='update':
        return redirect('/ticket-details/'+ str(ticketid))
    elif userInfo['role'] =='manager':
        return redirect(url_for('get_manager_tickets'))
    elif userInfo['role']=='admin':
        return redirect(url_for('get_all_tickets'))

################################### Ticket Detail ###############################################
# Endpoint fetches a specific ticket from the database and displays it.                         #
# Fetches -> ticket details, ticket history and comments                                        #
# Renders -> ticket-detail.html (accessable by all users)                                       #
#################################################################################################

@app.route('/ticket-details/<int:ticket_id>')
def get_ticket_details(ticket_id):
    userInfo = session.get('userProfile')
    
    # Fetch ticket record from tickets table
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404)

    # Fetch all the history record for this specific ticket from the ticket_history table
    #Join ticket_history, users on id to fetch user names
    detail = Ticket_history.query.join(Users,Ticket_history.users_id == Users.users_id,isouter=True)\
        .add_columns(Ticket_history.t_id,Ticket_history.t_status,Ticket_history.t_update_date, Ticket_history.priority,Users.users_name.label('users_id'))\
            .filter(Ticket_history.t_id == ticket_id)

    detail = [Ticket_history.format(row) for row in detail]
    
    # Fetch all the commnets for this specific ticket from the comments table
    #Join comment, users on id to fetch user names.
    comment = Comment.query.join(Users, Comment.users_id==Users.users_id)\
                .add_columns(Comment.t_id, Comment.comment, Comment.date, Users.users_name.label('users_id'))\
                .filter(Comment.t_id==ticket_id).all()
    comment = [Comment.format(co) for co in comment]

    #Fetch all the people in the project
    #join map_users_proj, Ticket on project id
    #join map_users_proj, Users on user id
    #Function is used to assign a user to specific ticket
    project_user = Ticket.query.join(Map_users_proj, Ticket.p_id == Map_users_proj.p_id)\
        .join(Users, Users.users_id == Map_users_proj.users_id)\
            .add_columns(Users.users_id, Users.users_name)\
                .filter(Ticket.t_id == ticket_id).filter(Users.users_role == 'dev').all()

    data = {
        'ticket': [ticket.format()],
        'detail': detail,
        'role': userInfo['role'],
        'user_name': userInfo['name'],
        'comment': comment,
        'page':'ticket_detail',
        'notify': notify(userInfo['id']),
        'project_user': project_user,
        'status':STATUS
    }
    return render_template('ticket-detail.html',data=data)

    ############################ Change Ticket Status ###########################################
# Endpoint is used to change the status of the Ticket                                       #
# Endpoint also records the status change in ticket history and notification table          #
# Requires -> ticket_id, projet_id, updated status                                          #
# Redirects -> ticket-details/{ticket_id}                                                   #
#############################################################################################

@app.route('/change-status', methods=['POST'])
def change_ticket_status():
    userInfo = session.get('userProfile')

    # Fetch all required information from the front end
    ticket_id = request.form.get('ticketid')
    project_id = request.form.get('projectid')
    status = request.form.get('status')
    t_date= date.today().strftime("%d/%m/%Y")

    # Fetch the ticket from the backend by the ticket_id
    ticket = Ticket.query.get(ticket_id)
    
    # if status changed that record it to ticket_history, notification table and add a comment
    if ticket.t_status != status:
        ticket_history = Ticket_history(ticket_id,ticket.users_id,status,t_date,ticket.t_priority)
        try: 
            ticket_history.insert()
        except:
            print(sys.exc_info())
            abort(500)
    
        project_user = Map_users_proj.query.with_entities(Map_users_proj.users_id).filter(Map_users_proj.p_id == project_id).all()
        for p in project_user:
            notify = Notification(ticket_id, p, type='update')
            try:
                notify.insert()
            except:
                print(sys.exc_info())
                abort(500)
        
        comment = "Satus changed to :" + status + " by :" + userInfo['name']
        comment = Comment(ticket_id,userInfo['id'],t_date,comment)
        try:
            comment.insert()
        except:
            print(sys.exc_info())
            abort(500)
    
    # if updated status = closed than update the close_date in the ticket table
    if ticket.t_status!=status and status == "closed":
        ticket.t_close_date=t_date
    
    # finally update the status in the ticket table
    ticket.t_status = status
    ticket.update()
    
    return redirect('/ticket-details/'+ str(ticket_id))
