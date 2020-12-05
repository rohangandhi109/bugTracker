import sys

from flask import Flask, redirect, jsonify,session,url_for
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


from models.TicketModel import Ticket
from models.EmpModel import Emp
from models.Map_emp_proj import Map_emp_proj
from models.ProjectModel import Project
from controllers import user, developer,ticket

@app.route('/')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    role = Emp.query.with_entities(Emp.emp_role).filter_by(emp_email=userinfo['email']).first()
    session['userProfile'] = {
        'email': userinfo['email'],
        'role': role[0],
        'name':userinfo['nickname']
    }
    if role[0] == 'user':
        return redirect('/my/tickets')
    elif role[0] == 'dev':
        return redirect('/dev/tickets')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('login', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.errorhandler(500)
def error_500(error):
    return jsonify({
    'success': False,
    'error': 500,
    'message': 'Server side error'
    }), 500

if __name__ == '__main__':
    app.run()
