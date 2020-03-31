from models import app
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user

# Helper funct
def error(err_locale, error):
  print(f'💩 Error in {err_locale}\n{error}')
  return jsonify(error='Server Error')

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    try:
      return get_all_users()
    except Exception as error:
      return error('GET /users route', error)
  if request.method == 'POST':
    try:
      return create_user(
        name=request.form['name'], 
        email=request.form['email'], 
        bio=request.form['bio']
      )
    except Exception as err:
      return error('POST /users route', error)


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_show_update_delete(id):
  if request.method == 'GET':
    try:
      return get_user(id)
    except Exception as error:
      return error('GET /users/:id route', error)
  if request.method == 'PUT':
    try:
      return update_user(
        id=id, 
        name=request.form['name'],
        email=request.form['email'],
        bio=request.form['bio']
      )
    except Exception as error:
      return error('PUT /users/:id route', error)
  if request.method == 'DELETE':
    try:
      return destroy_user(id)
    except Exception as error:
      return error('DELETE /users/:id route', error)