import numpy as np
import math
from app import app,db
from flask import abort,session,render_template,redirect,url_for,jsonify
from sqlalchemy import func,text

from models.Ticket import Ticket
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Users import Users
from models.MonthConfig import MonthConfig
from controllers import notification


@app.route('/manager/dashboard')
def manager_dashboard():
    userInfo = session.get('userProfile', 'not set')

    # Query to fetch open tickets
    openTickets = Ticket.query.join(Map_users_proj, Map_users_proj.p_id==Ticket.p_id)\
                    .with_entities(func.count(Ticket.t_id).label('count'))\
                    .filter(Map_users_proj.users_id==userInfo['id'])\
                    .filter(Ticket.t_status=='open')\
                    .filter(Map_users_proj.users_role=='manager')\
                    .one()
    openTickets = openTickets[0]

    #query to get unassigned tickets
    unassignedTickets = Ticket.query.join(Map_users_proj, Map_users_proj.p_id==Ticket.p_id)\
                        .with_entities(func.count(Ticket.t_id).label('count'))\
                        .filter(Map_users_proj.users_id==userInfo['id'])\
                        .filter(Ticket.users_id==0)\
                        .filter(Map_users_proj.users_role=='manager')\
                        .one()
    unassignedTickets = unassignedTickets[0]
    
    # Ticket with status in-progess
    assignedTickets = Ticket.query.join(Map_users_proj, Map_users_proj.p_id==Ticket.p_id)\
                    .with_entities(func.count(Ticket.t_id).label('count'))\
                    .filter(Map_users_proj.users_id==userInfo['id'])\
                    .filter(Ticket.t_status=='in-progress')\
                    .filter(Map_users_proj.users_role=='manager')\
                    .one()
    assignedTickets = assignedTickets[0]

    #Query to get average time for ticket completion
    sql = text(""" select cast(avg_ticket_time as INTEGER)
            from (select avg(diff) as avg_ticket_time 
            from (select (to_date(t_close_date,'DD/MM/YYYY') - to_date(t_create_date,'DD/MM/YYYY')) as diff 
            from ticket where t_status='closed')x)y; """)

    timePerTicket = db.session.execute(sql)
    timePerTicket = [row for row in timePerTicket]
    timePerTicket = timePerTicket[0][0]

    project = Project.query.join(Map_users_proj, Map_users_proj.p_id == Project.p_id)\
                .add_columns(Project.p_id, Project.p_name)\
                    .filter(Map_users_proj.users_id==userInfo['id'])
    data={
        'openTickets': openTickets,
        'unassignedTickets': unassignedTickets,
        'assignedTickets': assignedTickets,
        'timePerTicket' : timePerTicket,
        'project' : project,
        'notify': notification.notify(userInfo['id']),
        'page': 'dashboard',
        'role':userInfo['role']
    }
    return render_template('dashboard.html',data=data)

@app.route('/manager/chart/<int:project_id>')
def get_bar_pie_chart(project_id):
    userInfo = session.get('userProfile', 'not set')
    if project_id==0:
        sql = text(""" SELECT mapid.mth_name          AS month, 
                        proj.p_name                 AS name,
                            mapid.p_id              AS p_id, 
                            COALESCE(filter.cnt, 0) AS cnt 
                        FROM   (SELECT  config.mth_name, 
                                        config.mth_id, 
                                        proj.p_id 
                                FROM   month_config config 
                                    CROSS JOIN (SELECT p_id 
                                                FROM   map_users_proj 
                                                WHERE  users_id = 6 
                                                    AND users_role = 'manager') proj) mapid 
                        LEFT JOIN (SELECT Count(filter.t_id)              AS cnt, 
                                        filter.p_id, 
                                        Date_part('month', filter.date) AS month 
                                    FROM   (SELECT  tick.t_id, 
                                                    tick.p_id, 
                                                    To_date(tick.t_create_date, 'DD/MM/YYYY') AS 
                                                    date 
                                            FROM   ticket tick 
                                            WHERE  p_id IN (SELECT p_id 
                                                            FROM   map_users_proj 
                                                            WHERE 
                                                            users_id = """ + str(userInfo['id']) + """ 
                                                            AND users_role = 'manager')) filter 
                                    GROUP  BY filter.p_id, 
                                            Date_part('month', filter.date)) filter 
                        ON mapid.mth_id = filter.month 
                            AND mapid.p_id = filter.p_id
                            INNER JOIN project proj on mapid.p_id = proj.p_id;  """)

        chart_data = db.session.execute(sql)
        chart_data =  [MonthConfig.format(row) for row in chart_data]
        back_chart_data ={
            'chart_data': chart_data,
            'totalProjects': math.trunc(len(chart_data)/12),
        }  
        return back_chart_data
    else:
        sql = text(""" SELECT mapid.mth_name       AS month, 
                        proj.p_name         AS name,
                          mapid.p_id              AS p_id, 
                          COALESCE(filter.cnt, 0) AS cnt 
                    FROM   (SELECT  config.mth_name, 
                                    config.mth_id, 
                                    proj.p_id 
                            FROM   month_config config 
                                CROSS JOIN (SELECT """+ str(project_id) + """ as p_id) proj) mapid 
                    LEFT JOIN (SELECT Count(filter.t_id)              AS cnt, 
                                      filter.p_id, 
                                      Date_part('month', filter.date) AS month 
                                FROM   (SELECT  tick.t_id, 
                                                tick.p_id, 
                                                To_date(tick.t_create_date, 'DD/MM/YYYY') AS 
                                                date 
                                        FROM   ticket tick 
                                        WHERE  p_id = """+ str(project_id) +""" ) filter 
                                GROUP  BY filter.p_id, 
                                        Date_part('month', filter.date)) filter 
                    ON mapid.mth_id = filter.month 
                    AND mapid.p_id = filter.p_id
                    INNER JOIN project proj on mapid.p_id = proj.p_id;  """)
        chart_data = db.session.execute(sql)
        chart_data =  [MonthConfig.format(row) for row in chart_data]   
        back_chart_data ={
            'chart_data': chart_data,
            'totalProjects': math.trunc(len(chart_data)/12),
            'project' : ['BugTrack']
        }   
        return back_chart_data

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