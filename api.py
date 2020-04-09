from models import app, User
from flask import jsonify, request, g
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user
from crud.post_crud import get_all_posts, get_post, create_post, destroy_post, update_post
from crud.tag_crud import get_all_tags, get_posts_by_tag, destroy_tag
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

auth = HTTPTokenAuth('Bearer')

# App setup
@app.errorhandler(Exception)
def unhandled_exception(e):
  app.logger.error('Unhandled Exception: %s', (e))
  message_str = e.__str__()
  return jsonify(message=message_str.split(':')[0])

@auth.verify_token
def verify_token(token):
  s = Serializer(app.config['SECRET_KEY'])
  try:
    data = s.loads(token)
    g.user = User.query.filter_by(id=data["id"]).first()
  except SignatureExpired:
    return False # valid token, but expired
  except BadSignature:
    return False # invalid token
  return True

@app.route('/auth/login', methods=['POST'])
def authenticate():
  if request.form['email'] is None or request.form['password'] is None:
    raise KeyError('Email and Password required')

  user = User.query.filter_by(email=request.form['email']).first()
  if user is None or not user.verify_password(request.form['password']):
    raise Exception("Unauthorized")
  g.user = user
  token = user.generate_token()
  return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/protected')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.name })

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    return get_all_users()
  if request.method == 'POST':
    print(request.form)
    return create_user(**request.form)

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_show_update_delete(id):
  if request.method == 'GET':
    return get_user(id)
  if request.method == 'PUT':
    return update_user(id, **request.form)
  if request.method == 'DELETE':
    return destroy_user(id)

@app.route('/posts', methods=['GET', 'POST'])
def post_index_create():
  if request.method == 'GET':
    return get_all_posts()
  if request.method == 'POST':
    post_dict = {**request.form}
    post_dict['tags'] = [tag.strip() for tag in request.form['tags'].split(',')]
    return create_post(**post_dict)

@app.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post_show_update_delete(id):
  if request.method == 'GET':
    return get_post(id)
  if request.method == 'PUT':
    update_deets = {**request.form}
    if request.form['tags']:
      update_deets['tags'] = [tag.strip() for tag in request.form['tags'].split(',')]
    # Love this
    return update_post(id, **update_deets)
  if request.method == 'DELETE':
    return destroy_post(id)

@app.route('/tags')
def tags_index():
  return get_all_tags()

# Main usage of Tag functionality
@app.route('/tags/<int:id>', methods=['GET', 'DELETE'])
def post_by_tag_destroy_tag(id):
  if request.method == 'GET':
    return get_posts_by_tag(id)
  if request.method == 'DELETE':
    return destroy_tag(id)
