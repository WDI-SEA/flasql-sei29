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
    print(f'⏰ Signature Expired')
    return False # valid token, but expired
  except BadSignature:
    print(f'🧨 Invalid Token')
    return False # invalid token
  return True

@app.route('/auth/login', methods=['POST'])
def authenticate():
  if request.json['email'] is None or request.json['password'] is None:
    raise KeyError('Email and Password required')

  user = User.query.filter_by(email=request.json['email']).first()

  if user is None or not user.verify_password(request.json['password']):
    raise Exception("Unauthorized")

  g.user = user
  token = user.generate_token()
  return jsonify(user=user.as_dict(), token=token.decode('ascii'), status_code=200)


@app.route('/api/protected')
@auth.login_required
def get_resource():
  return jsonify({ 'data': 'Hello, %s!' % g.user.name })

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    return get_all_users()
  if request.method == 'POST':
    print(f'🍑 {request.json}')
    return create_user(**request.json)

@app.route('/users/<int:id>')
def user_show(id):
  return get_user(id)

@app.route('/users/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
def user_show_update_delete(id):
  if request.method == 'PUT':
    return update_user(id, **request.json)
  if request.method == 'DELETE':
    return destroy_user(id)

@app.route('/posts')
def post_index():
  return get_all_posts()

@app.route('/posts', methods=['POST'])
@auth.login_required
def post_create():
  post_dict = {**request.json}
  if request.json.get('tags') is not None:
    post_dict['tags'] = [tag.strip() for tag in request.json['tags'].split(',')]
  return create_post(**post_dict)

@app.route('/posts/<int:id>')
def post_show(id):
  return get_post(id)

@app.route('/posts/<int:id>', methods=['PUT', 'DELETE'])
@auth.login_required
def post_update_delete(id):
  if request.method == 'PUT':
    update_deets = {**request.json}
    if request.json.get('tags') is not None:
      update_deets['tags'] = [tag.strip() for tag in request.json['tags'].split(',')]
    # Love this
    return update_post(id, **update_deets)
  if request.method == 'DELETE':
    return destroy_post(id)

@app.route('/tags')
def tags_index():
  return get_all_tags()

# Main usage of Tag functionality
@app.route('/tags/<int:id>')
def index_posts_by_tag(id):
  return get_posts_by_tag(id)

@app.route('/tags/<int:id>', methods=['DELETE'])
@auth.login_required
def destroy_tag(id):
  return destroy_tag(id)
