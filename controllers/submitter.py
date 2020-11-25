from app import app
from models.TicketModel import Ticket
from flask import abort, request, jsonify
import sys


@app.route('/ticket', methods=['POST'])
def submit():
    body = request.get_json()
    t_title = body.get('t_title', '')
    t_desc = body.get('t_desc','')
    emp_id = body.get('emp_id', '')
    t_submitter = body.get('t_submitter','')
    p_id = body.get('p_id','')
    t_priority = body.get('t_priority','')
    t_status = body.get('t_status','')
    t_type = body.get('t_type','')
    t_create_date = body.get('t_create_date','')
    t_close_date = body.get('t_close_date','')

    ticket = Ticket(t_title, t_desc, emp_id, t_submitter, p_id, t_priority, t_status, t_type, t_create_date, t_close_date)
    try:
        ticket.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return jsonify({
            'success': True
        }), 201

