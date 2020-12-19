from app import app
from models.Users import Users
from models.Project import Project
from models.Ticket import Ticket
from models.Map_users_proj import Map_users_proj
from flask import render_template,session,request,abort,redirect,url_for
from datetime import date
import sys

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
    print(name)
    user = Users(email,name,name,role,create_date)
    print('done')
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
    
    # Get all the projects 
    project = Project.query.join(Map_users_proj, Map_users_proj.p_id==Project.p_id)\
        .add_columns(Project.p_id.label('id'), Project.p_name.label('name'))\
            .filter(Map_users_proj.users_id==Id)
    
    # Get the tickets of the user/dev/manager
    ticket = ""
    if user['role']=='user':
        ticket = Ticket.query.join(Project, Ticket.p_id==Project.p_id)\
            .add_columns(Ticket.t_id.label('id'), Ticket.t_title.label('title'), Project.p_name.label('project'))\
                .filter(Ticket.submitter_email==user['email'])
    elif user['role']=='dev':
        ticket = Ticket.query.join(Project, Ticket.p_id==Project.p_id)\
            .add_columns(Ticket.t_id.label('id'), Ticket.t_title.label('title'), Project.p_name.label('project'))\
                .filter(Ticket.users_id==Id)

    data = {
        'users' : [user],
        'projects': project,
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