import sys

from flask import Flask, redirect, jsonify,session,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from info import *


app = Flask(__name__)
app.secret_key = "something"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

oauth = OAuth(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET, PATCH, POST, DELETE, OPTIONS')
    return response

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

from models.Ticket import Ticket
from models.Users import Users
from models.Map_users_proj import Map_users_proj
from models.Project import Project
from models.Ticket_history import Ticket_history
from models.Notification import Notification
from models.Comment import Comment
from models.MonthConfig import MonthConfig
from controllers import user, developer,ticket,comment,project,Admin,manager

@app.route('/')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    users = Users.query.filter_by(users_email=userinfo['email']).first()
    users = users.format()
    session['userProfile'] = {
        'email': userinfo['email'],
        'role': users['role'],
        'name':userinfo['nickname'],
        'id':users['id']
    }
    if(users['role'] == "admin"):
        return redirect('/'+ users['role']+ '/users')
    if users['role'] == "manager":
        return redirect('/'+ users['role']+ '/dashboard')
    return redirect('/'+ users['role']+ '/tickets')

@app.route('/card')
def temp():
    return render_template('charts.html')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('login', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.errorhandler(404)
def error_404(error):
    return jsonify({
    'success': False,
    'error': 404,
    'message': 'Page not found'
    }), 404

@app.errorhandler(500)
def error_500(error):
    return jsonify({
    'success': False,
    'error': 500,
    'message': 'Server side error'
    }), 500

@app.errorhandler(401)
def error_401(error):
    return jsonify({
    'success': False,
    'error': 401,
    'message': 'unauthorized'
    }), 401

if __name__ == '__main__':
    app.run()
