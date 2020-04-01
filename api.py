from models import app
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user

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
    return create_user()


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_show_update_delete(id):
  if request.method == 'GET':
    return get_user(id)
  if request.method == 'PUT':
    return update_user(
      id=id, 
      name=request.form['name'],
      email=request.form['email'],
      bio=request.form['bio']
    )
  if request.method == 'DELETE':
    return destroy_user(id)
