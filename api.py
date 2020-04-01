from models import app
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user
from crud.post_crud import get_all_posts, get_post, create_post, destroy_post, update_post

@app.errorhandler(Exception)
def unhandled_exception(e):
  app.logger.error('Unhandled Exception: %s', (e))
  message_str = e.__str__()
  return jsonify(message=message_str.split(':')[0])

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
    return update_post(id, **request.form)
  if request.method == 'DELETE':
    return destroy_post(id)
