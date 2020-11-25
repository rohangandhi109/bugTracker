from app import app
from models.TicketModel import Ticket
from flask import abort, request, jsonify
import sys
from datetime import date


@app.route('/ticket', methods=['POST'])
def submit():
    t_title = request.form.get('t_title', '')
    t_desc = request.form.get('t_desc','')
    emp_id = 0
    t_submitter = "some"
    p_id = 0
    t_priority = request.form.get('t_priority','')
    t_status = "open"
    t_type = request.form.get('t_type','')
    t_create_date = date.today().strftime("%d/%m/%Y")
    t_close_date = "N/A"

    ticket = Ticket(t_title, t_desc, emp_id, t_submitter, p_id, t_priority, t_status, t_type, t_create_date, t_close_date)
    try:
        ticket.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return jsonify({
            'success': True
        }), 201

