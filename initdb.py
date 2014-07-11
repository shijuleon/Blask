#Import needed for instances of libraries
from blog import *

#Create an engine and connect, enable logging
from sqlalchemy import create_engine
engine = create_engine('sqlite:///blog.db', echo=True)

#Make a base to map the classes
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#Classes to map
class Posts(Base):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    pub_dtime = db.Column(db.Integer, default=datetime.now().strftime("%A, %B %d, %Y, %H:%M"))

    def __repr__(self):
        return '<id %r>' % self.id

#Create the database and tables
Base.metadata.create_all(engine)
