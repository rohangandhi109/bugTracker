from app import app
from models.TicketModel import Ticket
from flask import abort, request,render_template,redirect,url_for
import sys
from datetime import date

@app.route('/tickets')
def getTickets():
    print(request)
    ticket = Ticket.query.filter_by(submitter_id=1).all()
    ticket = [tick.format() for tick in ticket]
    return render_template('tickets.html', ticket=ticket)

@app.route('/ticket-form', methods=['GET'])
def getForm():
    return render_template('ticket-form.html')

@app.route('/ticket-form', methods=['POST'])
def submitTicket():
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    emp_id = 0
    submitter_id = 1
    p_id = 0
    t_priority = request.form.get('t_priority','')
    t_status = "open"
    t_type = request.form.get('t_type','')
    t_create_date = date.today().strftime("%d/%m/%Y")
    t_close_date = "N/A"

    ticket = Ticket(t_title, t_desc, emp_id, submitter_id, p_id, t_priority, t_status, t_type, t_create_date, t_close_date)
    try:
        ticket.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return redirect(url_for('getTickets'))
