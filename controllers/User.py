from app import app
from models.TicketModel import Ticket
from models.ProjectModel import Project
from models.EmpModel import Emp
from flask import abort, request,render_template,redirect,url_for,session
import sys
from datetime import date

@app.route('/my/tickets')
def get_tickets():
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']
    ticket = Ticket.query.filter_by(submitter_email=user_email).all()
    ticket = [tick.format() for tick in ticket]
    data={
        'ticket' : ticket,
        'user_email': userInfo['name']      
    }
    print(userInfo)
    return render_template('tickets.html', data=data)



@app.route('/my/logout')
def my_logout():
    return redirect(url_for('logout'))