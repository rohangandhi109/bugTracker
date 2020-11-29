import sys

from flask import Flask, redirect, jsonify,session,url_for
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


AUTH0_CALLBACK_URL = 'http://127.0.0.1:5000/callback'
AUTH0_CLIENT_ID = '2Qo9NMZBSqfdIvmx5Oeh2v0AGTKL61bB'
AUTH0_CLIENT_SECRET = 'YoMyvqDqWOP9IAWSv1HwQ_vjnK5wK_tJFDhRd0X39vkOy_Vfq7O78G84BWduc7nJ'
AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = 'bugTracker'

app = Flask(__name__)
app.secret_key = "something"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bug"
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
from controllers import User

@app.route('/')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session['userInfo'] = userinfo

    return redirect('/tickets')

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
