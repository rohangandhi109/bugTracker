from app import app,db
from models.Ticket import Ticket
from models.Project import Project
from models.Users import Users
from models.Ticket_history import Ticket_history
from models.Map_users_proj import Map_users_proj
from models.Notification import Notification
from controllers.notification import notify
from models.Comment import Comment
from flask import abort, request,render_template,redirect,url_for,session
import sys
from datetime import date
from sqlalchemy import text

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
        'priority':['High','low','Medium'],
        'status':['open','closed','on-hold']
    }
    return render_template('ticket-form.html',data=data)

@app.route('/update-ticket', methods=['POST'])
def create_ticket():
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
    if action=='new':
        ticket = Ticket(t_title, t_desc, users_id, submitter_email, p_id, t_priority, 'open', t_type, t_create_date, t_close_date)
        try:
            ticket.insert()
        except:
            print(sys.exc_info())
            abort(500)
        
        ticketid = ticket.t_id
        ticket_history = Ticket_history(ticket.t_id,users_id,'open',t_create_date,t_priority)
        
        try:
            ticket_history.insert()
        except:
            print(sys.exc_info())
            abort(500)

    if action=='update':
        ticketid = request.form.get('ticketid')
        ticket = Ticket.query.get(ticketid)
        t_date = date.today().strftime("%d/%m/%Y")
        t_status = request.form.get('t_status')
        
        # Insert into hsitory table:
        if ticket.t_status != t_status or ticket.t_priority!= t_priority:
            ticket_history = Ticket_history(ticketid,ticket.users_id,t_status,t_date,t_priority)
            try:
                ticket_history.insert()
            except:
                print(sys.exc_info())
                abort(500)

        if ticket.t_status!='closed' and t_status=='closed':
            ticket.t_close_date = date.today().strftime("%d/%m/%Y")
        ticket.t_title = t_title
        ticket.t_desc = t_desc
        ticket.t_status = t_status
        ticket.t_priority = t_priority
        ticket.t_status = t_status
        ticket.t_type = t_type 
        ticket.update()
        ticketid = ticket.t_id
    
    # send notification to all project people regardless of update or add
    project_user = Map_users_proj.query.with_entities(Map_users_proj.users_id).filter(Map_users_proj.p_id == p_id).all()
    for p in project_user:
        notify = Notification(ticketid, p, type=action)
        try:
            notify.insert()
        except:
            print(sys.exc_info())
            abort(500)

    if userInfo['role'] == 'dev':
        return redirect(url_for('get_project_tickets'))
    elif userInfo['role'] == 'user':
        return redirect(url_for('get_tickets'))
    elif action=='update':
        return redirect('/ticket-details/'+ str(ticketid))
    else:
        return redirect(url_for('get_all_tickets'))
    
@app.route('/ticket-details/<int:ticket_id>')
def get_ticket_details(ticket_id):
    userInfo = session.get('userProfile')
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404)

    detail = Ticket_history.query.join(Users,Ticket_history.users_id == Users.users_id,isouter=True)\
        .add_columns(Ticket_history.t_id,Ticket_history.t_status,Ticket_history.t_update_date, Ticket_history.priority,Users.users_name.label('users_id'))\
            .filter(Ticket_history.t_id == ticket_id)

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
        'notify': notify(userInfo['id']),
        'project_user': project_user,
        'status':['open','closed','on-hold']
    }
    return render_template('ticket-detail.html',data=data)

    