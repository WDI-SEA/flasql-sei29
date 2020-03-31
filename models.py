from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flasql'
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(150))

  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f'User(id={self.id}, email="{self.email}", name="{self.name}", bio="{self.bio}")'

  def as_dict(self):
    for c in self.__table__.columns:
      print(f"💽 c is {c}")
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  

post_tags = db.Table('post_tags',
  db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
  db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  header = db.Column(db.String(150), unique=True, nullable=False)
  body = db.Column(db.String, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

  tags = db.relationship('Tag',
    secondary=post_tags,
    lazy='subquery',
    backref=db.backref('posts', lazy=True)
  )

  def __repr__(self):
    return f'Post(id={self.id}, header="{self.header}", body="{self.body}", author_id={self.author_id})'


class Tag(db.Model):
  __tablename__ = 'tags'
  
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(50), unique=True, nullable=False)

  def __repr__(self):
    return f'Tag(id={self.id}, tag="{self.tag}")'