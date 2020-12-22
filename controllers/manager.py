from app import app
from flask import abort,session,render_template,redirect,url_for

from models.Ticket import Ticket
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Users import Users
from controllers import notification


@app.route('/manager/tickets')
def get_manager_tickets():

    #Authorize Manager
    userInfo = session.get('userProfile', 'not set')
    manager_email = userInfo['email']
    if userInfo['role'] != 'manager':
        abort(401)

    ticket = Ticket.query.join(Map_users_proj, Map_users_proj.p_id==Ticket.p_id)\
        .join(Users, Users.users_id==Map_users_proj.users_id)\
            .join(Project, Project.p_id==Map_users_proj.p_id)\
            .add_columns(Ticket.t_id.label('id'), Ticket.t_title.label('title'), Ticket.t_desc.label('desc'),\
                Project.p_name.label('p_id'), Ticket.t_priority.label('priority'),\
                Ticket.t_status.label('status'), Users.users_name.label('users_id'),\
                Ticket.t_create_date.label('create_date'),Ticket.t_close_date.label('close_date'))\
            .filter(Users.users_email==manager_email)
    
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'notify': notification.notify(userInfo['id']),
        'tickets_type' : 'all'
    }
    
    return render_template('list.html',data=data)

@app.route('/manager/my-tickets')
def get_manager_submitted_tickets():
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']
    if userInfo['role'] != 'manager':
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

@app.route('/manager/projects')
def get_manager_project():
    return redirect(url_for('get_dev_project'))