from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

user = "postgres"
pwd = 'postgres'
host = 'localhost'
port = '5432'
database_name = "fsnd_capstone"
database_path = "postgres://{}:{}@{}:{}/{}".format(
  user, pwd, host, port, database_name
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
