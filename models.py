# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from sqlalchemy import Column, Enum, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

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
    Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


actors = db.Table(
    'actors',
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movie.id'),
        primary_key=True
    ),
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actor.id'),
        primary_key=True
    )
)


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary=actors,
        lazy='subquery',
        backref=db.backref('movies', lazy=True)
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bday = Column(DateTime, nullable=False)
    gender = Column(Enum('M', 'F', name='gender_types'), default='M')

    def __init__(self, name, bday, gender):
        self.name = name
        self.bday = bday
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'bday': self.bday,
          'gender': self.gender,
        }
