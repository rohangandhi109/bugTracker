import sys
from datetime import date
from flask import render_template,session,request,abort,redirect,url_for
from sqlalchemy import text,func
from app import app,db

from models.Users import Users
from models.Project import Project
from models.Ticket import Ticket
from models.Map_users_proj import Map_users_proj

@app.route('/admin/users')
def get_all_users():
    userInfo = session.get('userProfile', 'not set')
    users = Users.query.filter(Users.users_role!="admin").all()
    users = [u.format() for u in users ]
    data = {
        'users' : users,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'users'
    }
    return render_template('list.html', data=data)


@app.route('/user-form')
def get_user_form():
    edit = request.args.get('edit','')
    userid = request.args.get('userid','')
    data =""
    rarray=['user','dev','manager']
    if edit=='true':
        user = Users.query.get(userid)
        data={
            'edit': 'true',
            'user':user.format(),
            'array': rarray
        }
    else:
        data={
            'edit':'false',
            'array': rarray
        }
    return render_template('user-form.html',data=data)

@app.route('/add-user',methods=['POST'])
def add_user():
    userInfo = session.get('userProfile')
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    role = request.form.get('role', '')
    create_date = date.today().strftime("%d/%m/%Y")
    
    new_id = db.session.query(func.max(Users.users_id))
    if new_id[0][0] == None:
        new_id[0][0]=0

    user = Users(new_id[0][0]+1,email,name,name,role,create_date)
    try:
        user.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return redirect(url_for('get_all_users'))

@app.route('/user-history/<int:Id>')
def get_user_history(Id):
    userInfo = session.get('userProfile', 'not set')
    # Get user details
    user = Users.query.get(Id)
    user = user.format()
    
    # Get all projects of the user
    project = Project.query.join(Map_users_proj, Map_users_proj.p_id==Project.p_id)\
        .add_columns(Project.p_id.label('id'), Project.p_name.label('name'))\
            .filter(Map_users_proj.users_id==Id)

    # Get all the projects
    all_project = Project.query.all()
    all_project = [p.format() for p in all_project]

    # Get the tickets of the user/dev/manager
    ticket = ""
    #user submitted tickets
    if user['role']=='user' or user['role']=='manager':
        ticket = Ticket.query.join(Project, Ticket.p_id==Project.p_id)\
            .add_columns(Ticket.t_id.label('id'), Ticket.t_title.label('title'), Project.p_name.label('project'))\
                .filter(Ticket.submitter_email==user['email'])
    #Developer Assigned tickets
    elif user['role']=='dev':
        ticket = Ticket.query.join(Project, Ticket.p_id==Project.p_id)\
            .add_columns(Ticket.t_id.label('id'), Ticket.t_title.label('title'), Project.p_name.label('project'))\
            .filter(Ticket.users_id==Id)

    data = {
        'users' : [user],
        'projects': project,
        'all_projects': all_project,
        'ticket': ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'userDetail'
    }
    return render_template('user-details.html',data=data)

@app.route('/delete-user')
def delete_user():
    userid = request.args.get('userid','')
    user = Users.query.get(userid)
    try:
        user.delete()
    except:
        print(sys.exc_info())
        abort(500)
    
    return redirect(url_for('get_all_users'))

@app.route('/edit-user',methods=['POST'])
def edit_user():
    userInfo = session.get('userProfile')
    id=request.form.get('id')
    user_update = Users.query.get(id)

    user_update.users_name = request.form.get('name', '')
    user_update.users_email = request.form.get('email', '')
    user_update.users_role = request.form.get('role', '')
    user_update.update()

    return redirect('/user-history/'+id)

@app.route('/assign-project', methods=['POST'])
def assign_project():
    user_id=request.form.get('user_id')
    project_id = request.form.get('project')
    role = request.form.get('role')
    assign_date = date.today().strftime("%d/%m/%Y")
    action_type = request.form.get('type')

    if action_type=='Assign':
        map = Map_users_proj(project_id,user_id,role,assign_date,'N/A')
        try:
            map.insert()
        except:
            print(sys.exc_info())
            abort(500)
    elif action_type=='Change':
        map = Map_users_proj.query.filter(Map_users_proj.users_id==user_id).filter(Map_users_proj.p_id==project_id).one()
        map.users_role=role
        map.update()

    project_details = request.form.get('project_details')
    if project_details=='true':
        return redirect('/project-details/'+project_id)
    else:
        return redirect('/user-history/'+user_id)

@app.route('/user-remove-project')
def remove_user_from_project():
    data = remove_from_project()
    return redirect('/user-history/'+data['user_id'])

@app.route('/remove-project-user')
def remove_project_user():
    data = remove_from_project()
    return redirect('/project-details/'+data['project_id'])


@app.route('/admin/projects')
def get_all_projects():
    userInfo = session.get('userProfile', 'not set')
    
    sql=text(""" SELECT proj.p_id         AS p_id, 
                                    proj.p_name       AS p_name, 
                                    proj.p_desc       AS p_desc, 
                                    proj.p_start_date AS p_start_date, 
                                    man.users_name     AS p_end_date 
                                FROM   project proj 
                                    LEFT OUTER JOIN (SELECT map.p_id, 
                                                            u.users_name 
                                                        FROM   map_users_proj map 
                                                            INNER JOIN users u 
                                                                    ON map.users_id = u.users_id 
                                                        WHERE  map.users_role = 'manager')man 
                                                    ON proj.p_id = man.p_id """)
                                                
    project = db.session.execute(sql)
    project = [Project.format(p) for p in project]
    data={
        'project' : project,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'projects'
    }
    return render_template('list.html',data=data)


def remove_from_project():
    user_id = request.args.get('userid')
    project_id = request.args.get('projectid')
    map = Map_users_proj.query.filter(Map_users_proj.p_id==project_id).filter(Map_users_proj.users_id==user_id).one()
    
    try:
        map.delete()
    except:
        print(sys.exc_info())
        abort(500)
    data = {
        'user_id':user_id,
        'project_id':project_id
    }
    return data

@app.route('/admin/tickets')
def get_all_tickets():
    userInfo = session.get('userProfile', 'not set')
    user_email=userInfo['email']
    ticket = Ticket.query.all()
    ticket = [Ticket.format(tick) for tick in ticket]
    data={
        'ticket' : ticket,
        'user_name': userInfo['name'],
        'role': userInfo['role'],
        'page' : 'tickets'
    }
    return render_template('list.html', data=data)

@app.route('/delete-ticket/<int:id>')
def delete_ticket(id):
    ticket = Ticket.query.get(id)
    try:
        ticket.delete()
    except:
        print(sys.exc_info())
        abort(500)
    return redirect('/admin/tickets')