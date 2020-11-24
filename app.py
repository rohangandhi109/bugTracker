from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

database_path = "postgres://postgres:postgres,localhost:5432/test"
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


@app.route('/')
def index():
    name = "ABC"
    demo = Demo(id=1, name=name)
    db.session.add(demo)
    db.session.commit()

    return 'hello world'


if __name__ == '__main__':
    app.run()
