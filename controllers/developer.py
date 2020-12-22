############################### Header ##############################################################
# Developer controller includes                                                                     #
# 1. all tickets of all projects of dev /dev/tickets                -> only dev can access          #
# 2. tickets assigned to the dev        /dev/assigned-tickets       -> only dev can access          #
# 3. Submited tickets                   /dev/my-tickets             -> only dev can access          #
# 4. assign a ticket to dev             /dev/assign-ticket          -> only dev can access          #
# 5. dev's project                      /dev/projects               -> only dev can access          #
# 6. change ticket status               /change-status              -> only dev can access          #
#####################################################################################################

from app import app,db
from models.Ticket import Ticket
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Ticket_history import Ticket_history
from models.Notification import Notification
from models.Comment import Comment
from models.Users import Users
from controllers import notification
from flask import abort, render_template,session, request,redirect, url_for
from datetime import date
from sqlalchemy import text
from auth import *
import sys

###################### Fetch tickets of all the project dev belongs #############################
# Endpoints generates a list tickets of all projects the dev belong to                          #
# Renders -> list.html (displays all the tickets in a table format)                             #
#################################################################################################

@app.route('/dev/tickets')
def get_project_tickets():
    
    #Authoraize the Developer
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)

    #Fetch query    
    sql = text("""SELECT tick.t_id, tick.t_title, tick.t_desc, tick.users_id, tick.submitter_email, tick.p_id, tick.t_priority, tick.t_status, tick.t_type, tick.t_create_date, tick.t_close_date
                FROM   ticket tick 
                INNER JOIN (SELECT map.p_id
                FROM   map_users_proj map 
                INNER JOIN (SELECT * FROM users WHERE  users_email = '""" + dev_email+ """')
                users ON map.users_id = users.users_id) filter 
                ON tick.p_id = filter.p_id  """)
    result = db.session.execute(sql)
    result = [row for row in result]
    ticket = [Ticket.format(row) for row in result]
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'all'
    }
    return render_template('list.html',data=data)


###################### Fetch tickets Assigned to the Developer ##################################
# Endpoints generates a list tickets that are assigned to the Developer                         #
# Renders -> list.html (displays all the tickets in a table format)                             #
#################################################################################################

@app.route('/dev/assigned-tickets')
def get_project_assigned_tickets():
    
    #Authoraize the Developer
    userInfo = session.get('userProfile', 'not set')
    if userInfo['role'] != 'dev':
        abort(401)

    # Fetch the tickets with same assigned developer id as the Developer    
    ticket = Ticket.query.filter(Ticket.users_id==userInfo['id']).all()
    ticket = ticket = [row.format() for row in ticket]
    
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'assigned'
    }
    return render_template('list.html',data=data)


###################### Fetch tickets submitted by Developer #####################################
# Endpoints generates a list tickets Submitted by Developer                                     #
# Renders -> list.html (displays all the tickets in a table format)                             #
#################################################################################################

@app.route('/dev/my-tickets')
def get_project_submitted_tickets():

    #Authoraize the Developer
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)

    # Fetch the tickets with same user_email as the Developer    
    ticket = Ticket.query.join(Project, Project.p_id==Ticket.p_id)\
            .add_columns(Ticket.t_id,Ticket.users_id,Ticket.submitter_email,\
            Ticket.t_title,Ticket.t_desc,Ticket.t_priority,Ticket.t_type,\
            Ticket.t_status,Ticket.t_create_date,Ticket.t_close_date,Project.p_name.label('p_id'))\
            .filter(Ticket.submitter_email==user_email).order_by(Ticket.t_id.asc()).all()
    ticket = [Ticket.format(tick) for tick in ticket]


    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'submitted'
    }
    return render_template('list.html', data=data)


################# Assign Ticket to Developer ################################################
# Endpoint is used to assign a specific ticket to specific developer                        #
# Endpoint as records this in the comments table and ticket_history table                   #
# requires -> user_id of assigned Developer and user_id of assigning Developer              #
# renders -> ticket-details/{ticket_id} (details of the ticket that are beign changed)      #
#############################################################################################

@app.route('/dev/assign-ticket',methods=['POST'])
def assign_dev_ticket():

    # Fetch the ticket that is to be assigned and assign the developer to it
    ticket = Ticket.query.get(request.form.get('ticket_id'))
    ticket.users_id = request.form.get('user_name')
    ticket.update()
    
    #insert Ticket History of assign the Devloper
    ticket_history = Ticket_history(ticket.t_id, ticket.users_id, ticket.t_status, date.today().strftime("%d/%m/%Y") , ticket.t_priority)
    try:
        ticket_history.insert()
    except:
        print('error')

    #insert comment of which User assigned the Dev
    userInfo = session.get('userProfile', 'not set')
    user1 = userInfo['id']
    user2 = Users.query.with_entities(Users.users_name).filter(Users.users_id == ticket.users_id).one()
    text = user2[0] + ' assigned to this ticket'
    comment = Comment(ticket.t_id, user1, date.today().strftime("%d/%m/%Y"), text)
    try:
        comment.insert()
    except:
        print(sys.exc_info())
    
    #Insert notification for assignnig the Dev
    notify = Notification(ticket.t_id, ticket.users_id,'assigned')
    try:
        notify.insert()
    except:
        print(sys.exc_info())
    

    return redirect('/ticket-details/'+ request.form.get('ticket_id'))


################################# Fetch all Developer projects ##############################
# Endpoint fetches list of projects of the developer                                        #
# Renders -> list.html (displays all the project in table format)                           #
#############################################################################################

@app.route('/dev/projects')
def get_dev_project():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']

    #fetch list of projects that the Developer is assigned to using the map table
    #join Project, map_users_proj on project id
    #join map_users_proj, users on user_id
    #The map_users_proj table contains the maping of project to user
    project = Project.query.join(Map_users_proj, Map_users_proj.p_id == Project.p_id)\
        .join(Users, Users.users_id == Map_users_proj.users_id).filter(Users.users_email == dev_email).all()
    project = [Project.format(pro) for pro in project]

    data={
        'project' : project,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'notify': notification.notify(userInfo['id']),
        'page' : 'projects'
    }
    return render_template('list.html',data=data)


############################ Change Ticket Status ###########################################
# Endpoint is used to change the status of the Ticket                                       #
# Endpoint also records the status change in ticket history and notification table          #
# Requires -> ticket_id, projet_id, updated status                                          #
# Redirects -> ticket-details/{ticket_id}                                                   #
#############################################################################################

@app.route('/change-status', methods=['POST'])
def change_ticket_status():

    # Fetch all required information from the front end
    ticket_id = request.form.get('ticketid')
    project_id = request.form.get('projectid')
    status = request.form.get('status')
    t_date= date.today().strftime("%d/%m/%Y")

    # Fetch the ticket from the backend by the ticket_id
    ticket = Ticket.query.get(ticket_id)
    
    # if status changed that record it to ticket_history and notification table
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
    
    # if updated status = closed than update the close_date in the ticket table
    if ticket.t_status!=status and status == "closed":
        ticket.t_close_date=t_date
    
    # finally update the status in the ticket table
    ticket.t_status = status
    ticket.update()
    
    return redirect('/ticket-details/'+ str(ticket_id))
