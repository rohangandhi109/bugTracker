from app import app,db
from models.Ticket import Ticket
from models.Project import Project
from models.Map_user_proj import Map_user_proj
from models.Users import Users
from flask import abort, request,render_template,redirect,url_for,session, jsonify
from datetime import date
from sqlalchemy import text
from auth import *

@app.route('/dev/tickets')
def get_project_tickets():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    if userInfo['role'] != 'dev':
        abort(401)
    sql = text("""SELECT tick.t_id, tick.t_title, tick.t_desc, tick.user_id, tick.submitter_email, tick.p_id, tick.t_priority, tick.t_status, tick.t_type, tick.t_create_date, tick.t_close_date
                FROM   ticket tick 
                INNER JOIN (SELECT map.p_id
                FROM   map_user_proj map 
                INNER JOIN (SELECT * FROM user WHERE  user_email = '""" + dev_email+ """')
                users ON map.user_id = user.user_id) filter 
                ON tick.p_id = filter.p_id  """)
    result = db.session.execute(sql)
    result = [row for row in result]
    ticket = [Ticket.format(row) for row in result]
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets' 
    }
    return render_template('tickets.html',data=data)

@app.route('/add-comment')
def add_comment():
    return ""
