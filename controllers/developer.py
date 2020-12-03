from app import app
from models.TicketModel import Ticket
from flask import abort, request,render_template,redirect,url_for,session, jsonify
from datetime import date


@app.route('/dev/tickets')
def get_project_tickets():
    data = []

    return render_template('tickets.html', data=data)
