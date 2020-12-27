######################################### Header ################################################
# User controller includes                                                                      #
# 1. View all submitted tickets     /user/tickets       only user can access                    #
#################################################################################################

import sys
from datetime import date
from flask import abort, request,render_template,redirect,url_for,session

from app import app

from models.Ticket import Ticket
from models.Project import Project
from models.Users import Users

################################### View All Tickets ##############################################
# Endpoint fetches all the tickets submitted by the user                                          #
# Renders -> list.html (displays all the tickets in a table format)                               #
###################################################################################################

@app.route('/user/tickets')
def get_tickets():
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']

    # AUthorize the user
    if userInfo['role'] != 'user':
        abort(401)

    # fetch list of tickets
    ticket = Ticket.query.join(Project, Project.p_id==Ticket.p_id)\
            .add_columns(Ticket.t_id,Ticket.users_id,Ticket.submitter_email,\
            Ticket.t_title,Ticket.t_desc,Ticket.t_priority,Ticket.t_type,\
            Ticket.t_status,Ticket.t_create_date,Ticket.t_close_date,Project.p_name.label('p_id'))\
            .filter(Ticket.submitter_email==user_email).order_by(Ticket.t_id.asc()).all()
    ticket = [Ticket.format(tick) for tick in ticket]
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets'
    }
    return render_template('list.html', data=data)

@app.route('/user/logout')
def my_logout():
    return redirect(url_for('logout'))