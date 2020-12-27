import sys
from datetime import datetime
from flask import redirect,request,session,abort

from app import app

from models.Comment import Comment
from models.Users import Users


@app.route('/add-comment',methods=['POST'])
def add_comment():
    ticket_id = request.form.get('ticket_id')
    comment = request.form.get('comment')
    date = datetime.today().strftime("%d/%m/%Y")
    users_id = Users.query.with_entities(Users.users_id).filter_by(users_email=session.get('userProfile')['email'])
    comment = Comment(ticket_id,users_id,date,comment)
    try:
        comment.insert()
    except:
        print(sys.exc_info())
        abort(500)
    return redirect('/ticket-details/'+ticket_id)