from app import app,db
from models.Ticket import Ticket
from models.Project import Project
from models.Users import Users
from models.Ticket_history import Ticket_history
from models.Map_users_proj import Map_users_proj
from models.Notification import Notification
from models.Comment import Comment
from flask import abort, request,render_template,redirect,url_for,session
import sys
from datetime import date
from sqlalchemy import text

@app.route('/ticket-form', methods=['GET'])
def get_ticketForm():
    project  = Project.query.all()
    project = [tick.format() for tick in project]
    data = {
        'project':project,
    }
    return render_template('ticket-form.html',data=data)

@app.route('/ticket-form', methods=['POST'])
def create_ticket():
    userInfo = session.get('userProfile')
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    users_id = 0
    submitter_email = userInfo['email']
    p_id = request.form.get('project')
    t_priority = request.form.get('t_priority','')
    t_status = "open"
    t_type = request.form.get('t_type','')
    t_create_date = date.today().strftime("%d/%m/%Y")
    t_close_date = "N/A"

    ticket = Ticket(t_title, t_desc, users_id, submitter_email, p_id, t_priority, t_status, t_type, t_create_date, t_close_date)
    try:
        ticket.insert()
    except:
        print(sys.exc_info())
        abort(500)
    
    ticket_history = Ticket_history(ticket.t_id,users_id,t_status,t_create_date,t_priority)
    
    try:
        ticket_history.insert()
    except:
        print(sys.exc_info())
        abort(500)

    project_user = Map_users_proj.query.with_entities(Map_users_proj.users_id).filter(Map_users_proj.p_id == p_id).all()
    for p in project_user:
        notify = Notification(ticket.t_id, p, type='new')
        try:
            notify.insert()
        except:
            print(sys.exc_info())
            abort(500)
    
    if userInfo['role'] == 'dev':
        return redirect(url_for('get_project_tickets'))
    elif userInfo['role'] == 'user':
        return redirect(url_for('get_tickets'))
    
@app.route('/ticket-details/<int:ticket_id>')
def get_ticket_details(ticket_id):
    userInfo = session.get('userProfile')
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404)
    sql = text("""SELECT tick_detail.t_id, 
                filter.users_name as users_id, 
                tick_detail.t_status, 
                tick_detail.t_update_date,
                tick_detail.priority
                FROM   ticket_history tick_detail 
                INNER JOIN (SELECT u.users_name, tick.t_id FROM users u
                LEFT OUTER JOIN (SELECT users_id, t_id FROM ticket WHERE  t_id = '"""+ str(ticket_id) +"""') tick 
                ON u.users_id = tick.users_id) filter 
                ON tick_detail.t_id = filter.t_id  """)
    detail = db.session.execute(sql)
    detail = [row for row in detail]
    detail = [Ticket_history.format(row) for row in detail]
    
    comment = Comment.query.join(Users, Comment.users_id==Users.users_id)\
                .add_columns(Comment.t_id, Comment.comment, Comment.date, Users.users_name.label('users_id'))\
                .filter(Comment.t_id==ticket_id).all()

    comment = [Comment.format(co) for co in comment]

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
        'project_user': project_user
    }
    return render_template('ticket-detail.html',data=data)

    