############################### Header ##############################################################
# Developer controller includes                                                                     #
# 1. all tickets of all projects of dev /dev/tickets                -> only dev can access          #
# 2. tickets assigned to the dev        /dev/assigned-tickets       -> only dev can access          #
# 3. Submited tickets                   /dev/my-tickets             -> only dev can access          #
# 4. assign a ticket to dev             /dev/assign-ticket          -> only dev can access          #
# 5. dev's project                      /dev/projects               -> only dev can access          #
#####################################################################################################
import sys
from datetime import date
from flask import abort, render_template,session, request,redirect, url_for
from sqlalchemy import func


from app import app,db
from info import DATE

from models.Ticket import Ticket
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Ticket_history import Ticket_history
from models.Notification import Notification
from models.Comment import Comment
from models.Users import Users

from controllers import notification

###################### Fetch tickets of all the project dev belongs #############################
# Endpoints generates a list tickets of all projects the dev belong to                          #
# Renders -> list.html (displays all the tickets in a table format)                             #
#################################################################################################

@app.route('/dev/tickets')
def get_project_tickets():
    
    #Authorise the Developer
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)

    #Fetch query    
    ticket = Ticket.query.join(Map_users_proj, Map_users_proj.p_id==Ticket.p_id)\
            .join(Users, Users.users_id==Map_users_proj.users_id)\
            .join(Project, Project.p_id==Map_users_proj.p_id)\
            .add_columns(Ticket.t_id.label('id'),Users.users_name.label('user_name'),Ticket.submitter_email.label('email'),\
                    Ticket.t_title.label('title'),Ticket.t_desc.label('desc'),Ticket.t_priority.label('priority'),\
                    Ticket.t_type.label('type'),Ticket.t_status.label('status'),Ticket.t_create_date.label('create_date'),\
                    Ticket.t_close_date.label('close_date'),Project.p_name.label('p_id'))\
            .filter(Users.users_email==dev_email)\
            .all()
    
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'all',
        'nav_bar':'alltickets'
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
    ticket = Ticket.query.join(Project, Project.p_id == Ticket.p_id)\
                .join(Users, Users.users_id==Ticket.users_id)\
                .add_columns(Ticket.t_id.label('id'),Users.users_name.label('user_name'),Ticket.submitter_email.label('email'),\
                    Ticket.t_title.label('title'),Ticket.t_desc.label('desc'),Ticket.t_priority.label('priority'),\
                    Ticket.t_type.label('type'),Ticket.t_status.label('status'),Ticket.t_create_date.label('create_date'),\
                    Ticket.t_close_date.label('close_date'),Project.p_name.label('p_id'))\
                .filter(Ticket.users_id==userInfo['id']).all()
    
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'assigned',
        'nav_bar':'assignedtickets'
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
                .join(Users, Users.users_id==Ticket.users_id)\
                .add_columns(Ticket.t_id.label('id'),Users.users_name.label('user_name'),Ticket.submitter_email.label('email'),\
                    Ticket.t_title.label('title'),Ticket.t_desc.label('desc'),Ticket.t_priority.label('priority'),\
                    Ticket.t_type.label('type'),Ticket.t_status.label('status'),Ticket.t_create_date.label('create_date'),\
                    Ticket.t_close_date.label('close_date'),Project.p_name.label('p_id'))\
                .filter(Ticket.submitter_email==user_email)
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'submitted',
        'nav_bar':'submittedtickets'
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

    userInfo = session.get('userProfile', 'not set')
    if userInfo['role'] !='dev':
        abort(401)
    # Fetch the ticket that is to be assigned and assign the developer to it
    ticket = Ticket.query.get(request.form.get('ticket_id'))
    ticket.users_id = request.form.get('user_name')
    ticket.update()
    
    #insert Ticket History of assign the Devloper
    new_id = db.session.query(func.max(Ticket_history.id))
    if new_id[0][0] == None:
        new_id[0][0]=0
    ticket_history = Ticket_history(new_id[0][0]+1,ticket.t_id, ticket.users_id, ticket.t_status, DATE , ticket.t_priority)
    try:
        ticket_history.insert()
    except:
        print('error')

    #insert comment of which User assigned the Dev
    userInfo = session.get('userProfile', 'not set')
    user1 = userInfo['id']
    user2 = Users.query.with_entities(Users.users_name).filter(Users.users_id == ticket.users_id).one()
    text = user2[0] + ' assigned to this ticket'
    new_id = db.session.query(func.max(Comment.c_id))
    if new_id[0][0] == None:
        new_id[0][0]=0
    comment = Comment(new_id[0][0]+1,ticket.t_id, user1, DATE, text)
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

    if userInfo['role'] !='dev' and userInfo['role'] != 'manager':
        abort(401)

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