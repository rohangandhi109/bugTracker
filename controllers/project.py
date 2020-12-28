##################################### Header ########################################################################
# Project controller includes                                                                                       #
#  1. Project details           /project-details/{project_id}           -> accessable to admin, Developer, Manager  #
#####################################################################################################################

import sys
from datetime import date
from flask import session, render_template,request,abort,redirect,url_for
from sqlalchemy import func

from app import app,db
from info import DATE

from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Ticket import Ticket
from models.Users import Users

from controllers import notification

@app.route('/project-form')
def get_project_form():
    return render_template('project-form.html')

@app.route('/create-project', methods=['POST'])
def create_project():
    userInfo = session.get('userProfile')
    name = request.form.get('name', '')
    desc = request.form.get('desc','')
    start_date = DATE

    new_id = db.session.query(func.max(Project.p_id)).one()
    print(new_id)
    if new_id[0] == None:
        new_id[0] = 0
    project = Project(new_id[0] + 1,name,desc,start_date,'N/A')
    try:
        project.insert()
    except:
        print(sys.exc_info())
        abort(500)

    return redirect(url_for('get_all_projects'))


######################### Project Details #######################################################################
# Endpoint is used to fetch the details of a specific project                                                   #
# Fetches -> Specific Project details, All Tickets Project, Users assigned to the project                       #
# Renders -> project-details.html                                                                               #
#################################################################################################################

@app.route('/project-details/<int:project_id>')
def get_project_details(project_id):

    userInfo = session.get('userProfile')
    
    # Fetch all the tickets of the project with project_id
    ticket = Ticket.query.filter(Ticket.p_id == project_id).all()
    ticket = [tick.format() for tick in ticket]

    # Fetch the users info assigned to the project
    # join Users, map_users_proj on user_id
    # join map_users_proj, Project on project_id
    # join is used to map the users to project table using the mapping table map_users_proj

    user = Users.query.join(Map_users_proj, Map_users_proj.users_id == Users.users_id)\
        .join(Project, Project.p_id == Map_users_proj.p_id)\
            .add_columns(Users.users_id.label('id'),Users.users_name.label('name'),Users.users_email.label('email'),Map_users_proj.users_role.label('role'))\
        .filter(Project.p_id == project_id).all()
    
    # Fetch the project records with primary key project_id
    project = Project.query.get(project_id)

    # Only authorized by the admin
    # fetch all the users lists 
    # this is used to add users to project/change role of specific user
    all_users=""
    if userInfo['role']=="admin":
        all_users = Users.query.all()
        all_users = [all.format() for all in all_users]

    data = {
        'users': user,
        'ticket': ticket,
        'project': project.format(),
        'all_users': all_users,
        'role': userInfo['role'],
        'user_name': userInfo['name'],
        'notify': notification.notify(userInfo['id']),
        'page':'project_detail'
    }
    return render_template('project-detail.html', data=data)