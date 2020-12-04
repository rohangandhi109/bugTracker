from app import app,db
from models.TicketModel import Ticket
from models.ProjectModel import Project
from models.Map_emp_proj import Map_emp_proj
from models.EmpModel import Emp
from flask import abort, request,render_template,redirect,url_for,session, jsonify
from datetime import date
from sqlalchemy import text
from auth import *

@app.route('/dev/tickets')
def get_project_tickets():
    userInfo = session.get('userProfile', 'not set')
    dev_email = userInfo['email']
    sql = text("""SELECT tick.t_id, tick.t_title, tick.t_desc, tick.emp_id, tick.submitter_email, tick.p_id, tick.t_priority, tick.t_status, tick.t_type, tick.t_create_date, tick.t_close_date
                FROM   ticket tick 
                INNER JOIN (SELECT map.p_id
                FROM   map_emp_proj map 
                INNER JOIN (SELECT * FROM emp WHERE  emp_email = '""" + dev_email+ """')
                emp ON map.emp_id = emp.emp_id) filter 
                ON tick.p_id = filter.p_id  """)
    result = db.session.execute(sql)
    result = [row for row in result]
    ticket = [Ticket.format(row) for row in result]
    data={
        'ticket' : ticket,
        'user_email': userInfo['name']     
    }
    return render_template('tickets.html',data=data)
