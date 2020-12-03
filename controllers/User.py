from app import app
from models.TicketModel import Ticket
from flask import abort, request,render_template,redirect,url_for,session
import sys
from datetime import date

@app.route('/my/tickets')
def get_tickets():
    userInfo = session.get('userInfo', 'not set')
    ticket = Ticket.query.filter_by(submitter_email='bob@gmail.com').all()
    ticket = [tick.format() for tick in ticket]
    data={
        'ticket' : ticket,
        'user_email': userInfo['nickname']      
    }
    return render_template('tickets.html', data=data)

@app.route('/ticket-form', methods=['GET'])
def get_ticketForm():
    return render_template('ticket-form.html')

@app.route('/ticket-form', methods=['POST'])
def create_ticket():
    userInfo = session.get('userInfo')
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    emp_id = 0
    submitter_email = userInfo['email'] 
    p_id = 0
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
    return redirect(url_for('get_tickets'))
