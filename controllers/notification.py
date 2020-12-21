from models.Notification import Notification
from app import app,db
from flask import request,redirect,url_for
import sys

def notify(id):
    notify = Notification.query.filter(Notification.users_id == id).all()
    notify = [no.format() for no in notify]
    return notify

@app.route('/delete-notification')
def deleteNotification():
    ticket_id = request.args.get('ticket')
    notify_id = request.args.get('notify')
    notify = Notification.query.get(notify_id)
    try:
        notify.delete()
    except:
        print(sys.exc_info())
    
    return redirect('/ticket-details/'+ ticket_id)