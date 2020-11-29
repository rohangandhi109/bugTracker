from functools import wraps
import constants
from flask import Flask, render_template, session, redirect
from os import environ as env
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv


AUTH0_CALLBACK_URL = 'http://127.0.0.1:5000/callback'
AUTH0_CLIENT_ID = '2Qo9NMZBSqfdIvmx5Oeh2v0AGTKL61bB'
AUTH0_CLIENT_SECRET = 'YoMyvqDqWOP9IAWSv1HwQ_vjnK5wK_tJFDhRd0X39vkOy_Vfq7O78G84BWduc7nJ'
AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = 'bugTracker'

app = Flask(__name__,  static_url_path='/static')
app.secret_key = 'constants.SECRET_KEY'

oauth = OAuth(app)

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

@app.route('/tickets')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    print(userinfo)
    return "user"



@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
