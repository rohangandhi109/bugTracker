from app import app
from models.TicketModel import Ticket
from models.ProjectModel import Project
from models.EmpModel import Emp
from flask import abort, request,render_template,redirect,url_for,session
import sys
from datetime import date

@app.route('/ticket-form', methods=['GET'])
def get_ticketForm():
    project  = Project.query.all()
    project = [tick.format() for tick in project]
    return render_template('ticket-form.html',project=project)

@app.route('/ticket-form', methods=['POST'])
def create_ticket():
    userInfo = session.get('userProfile')
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    emp_id = Emp.query.with_entities(Emp.emp_id).filter_by(emp_email=userInfo['email']).one()
    submitter_email = userInfo['email']
    p_id = request.form.get('project')
    t_priority = request.form.get('t_priority','')
    t_status = "open"
    t_type = request.form.get('t_type','')
    t_create_date = date.today().strftime("%d/%m/%Y")
    t_close_date = "N/A"

    ticket = Ticket(t_title, t_desc, emp_id, submitter_email, p_id, t_priority, t_status, t_type, t_create_date, t_close_date)
    try:
        ticket.insert()
    except:
        print(sys.exc_info())
        abort(500)
    if userInfo['role'] == 'dev':
        return redirect(url_for('get_project_tickets'))
    elif userInfo['role'] == 'user':
        return redirect(url_for('get_tickets'))
    