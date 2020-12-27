######################### Header ############################################################################
# Notification is given to all the developers and project manager                                           #
# Notified about new ticket, ticket update, ticket assigned                                                 #
# Notification controller includes                                                                          #
# 1. fetches list of notification   function notify()               accessed by Developers and Managers     #
# 2. deletes a notification         Endpoint /delete-notification   accessed by Developers and Managers     #
#############################################################################################################

import sys
from flask import request,redirect,url_for

from app import app

from models.Notification import Notification


################## Fetch list of notification ###################################################
# Function to fetch list of notification of a specific user                                     #
# Requires -> user_id                                                                           #
# Returns -> n: list of notification and length: number of notification                         #
#################################################################################################

def notify(id):
    notification = Notification.query.filter(Notification.users_id == id).all()
    notification = [no.format() for no in notification]
    notify = {
        'list': notification,
        'length' : len(notification)
    }
    return notify

################### Delete a notification ###########################################################
# Endpoint that deletes a specific notifcation                                                      #
# Requires -> notification_id                                                                       #
# Redirects -> /ticket-details/{ticket_id}                                                          #
#####################################################################################################

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