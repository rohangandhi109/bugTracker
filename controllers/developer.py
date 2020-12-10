from app import app,db
from models.Ticket import Ticket
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Users import Users
from flask import abort, render_template,session, request,redirect, url_for
from datetime import date
from sqlalchemy import text
from auth import *
import json

@app.route('/dev/tickets')
def get_project_tickets():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)
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
        'tickets_type' : 'all'
    }
    return render_template('list.html',data=data)

@app.route('/dev/assigned-tickets')
def get_project_assigned_tickets():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)
    ticket = Ticket.query.filter(Ticket.users_id==userInfo['id']).all()
    ticket = ticket = [row.format() for row in ticket]
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets',
        'tickets_type' : 'assigned'
    }
    return render_template('list.html',data=data)

@app.route('/dev/my-tickets')
def get_project_submitted_tickets():
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)
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
        'tickets_type' : 'submitted'
    }
    return render_template('list.html', data=data)

@app.route('/dev/assign-ticket',methods=['POST'])
def assign_dev_ticket():
    ticket = Ticket.query.get(request.form.get('ticket_id'))
    ticket.users_id = request.form.get('user_name')
    ticket.update()
    return redirect('/ticket-details/'+ request.form.get('ticket_id'))

@app.route('/dev/projects')
def get_dev_project():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    project = Project.query.join(Map_users_proj, Map_users_proj.p_id == Project.p_id)\
        .join(Users, Users.users_id == Map_users_proj.users_id).filter(Users.users_email == dev_email).all()
    project = [Project.format(pro) for pro in project]

    data={
        'project' : project,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'projects'
    }
    return render_template('list.html',data=data)

