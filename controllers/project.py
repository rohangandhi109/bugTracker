from app import app
from models.Project import Project
from models.Map_users_proj import Map_users_proj
from models.Ticket import Ticket
from models.Users import Users
from flask import session, render_template

@app.route('/project-details/<int:project_id>')
def get_project_details(project_id):

    userInfo = session.get('userProfile')
    
    ticket = Ticket.query.filter(Ticket.p_id == project_id).all()
    ticket = [tick.format() for tick in ticket]

    user = Users.query.join(Map_users_proj, Map_users_proj.users_id == Users.users_id)\
        .join(Project, Project.p_id == Map_users_proj.p_id)\
            .add_columns(Users.users_name.label('name'),Users.users_email.label('email'),Map_users_proj.users_role.label('role'))\
        .filter(Project.p_id == project_id).all()
    
    project = Project.query.get(project_id)

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
        'page':'project_detail'
    }
    return render_template('project-detail.html', data=data)