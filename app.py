import sys

from flask import Flask, redirect, jsonify,session,url_for
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from info import *
from auth import verify_decode_jwt

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
from controllers import user

@app.route('/')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/callback')
def callback_handling():
    auth = auth0.authorize_access_token()
    payload = verify_decode_jwt(auth['access_token'])
    print(payload)
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session['userInfo'] = userinfo
    
    return redirect('/my/tickets')

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
