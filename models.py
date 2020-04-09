from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_cors import CORS

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flasql'
app.config['SECRET_KEY'] = 'some_SUpER_SecREt_str1NG'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(150))
  password = db.Column(db.String, nullable=False)

  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f'User(id={self.id}, email="{self.email}", name="{self.name}", bio="{self.bio}")'
  
  def as_dict(self):
    user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    del user_dict['password']
    return user_dict

  def set_password(self, password):
    self.password = pwd_context.encrypt(password)

  def verify_password(self, typed_password):
    return pwd_context.verify(typed_password, self.password)

  # expiration time is in seconds
  def generate_token(self, expiration=60*10):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({ 'id': self.id })
  

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

  def as_dict(self):
    return {
      'id': self.id,
      'header': self.header,
      'body': self.body,
      'author': self.author.as_dict()['name'],
    }


class Tag(db.Model):
  __tablename__ = 'tags'
  
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(50), unique=True, nullable=False)

  def __repr__(self):
    return f'Tag(id={self.id}, tag="{self.tag}")'
  
  def as_dict(self):
    return {'id': self.id, 'tag': self.tag}


def get_or_create(model, defaults=None, **kwargs):
  instance = db.session.query(model).filter_by(**kwargs).first()
  if instance:
    return instance, False
  else:
    params = dict((k, v) for k, v in kwargs.items())
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    db.session.commit()
    return instance, True