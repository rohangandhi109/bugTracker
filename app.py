import sys

from flask import Flask, redirect, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'
API_AUDIENCE = 'bugTracker'
AUTH0_CLIENT_ID = '2Qo9NMZBSqfdIvmx5Oeh2v0AGTKL61bB'
AUTH0_CALLBACK_URL = 'http://127.0.0.1:5000/tickets'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bug"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET, PATCH, POST, DELETE, OPTIONS')
    return response

@app.route("/", methods=["GET"])
def generate_auth_url():
    
    url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'

    return redirect(url)

@app.route("/login")
def login():
    return render_template('login.html')

from models.TicketModel import Ticket
from controllers import User


@app.errorhandler(500)
def error_500(error):
    return jsonify({
    'success': False,
    'error': 500,
    'message': 'Server side error'
    }), 500

if __name__ == '__main__':
    app.run()
