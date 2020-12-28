import sys
from datetime import datetime
from flask import redirect,request,session,abort
from sqlalchemy import func

from app import app,db
from info import DATE

from models.Comment import Comment
from models.Users import Users


@app.route('/add-comment',methods=['POST'])
def add_comment():
    ticket_id = request.form.get('ticket_id')
    comment = request.form.get('comment')
    date = DATE
    users_id = Users.query.with_entities(Users.users_id).filter_by(users_email=session.get('userProfile')['email'])
    
    new_id = db.session.query(func.max(Comment.c_id))
    if new_id[0][0] == None:
        new_id[0][0]=0

    comment = Comment(new_id[0][0]+1,ticket_id,users_id,date,comment)
    try:
        comment.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return redirect('/ticket-details/'+ticket_id)