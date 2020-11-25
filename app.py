import sys

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result


@app.route('/')
def index():
    try:
        result = Result("rohan",123)
        db.session.add(result)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return 'hello world'

@app.route('/temp')
def hello():
    temp = Result.query.all()
    temp = [tmp.format() for tmp in temp]

    return jsonify(temp),200


if __name__ == '__main__':
    app.run()
