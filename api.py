from models import app
from helpers import InvalidUsage
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    try:
      return get_all_users()
    except Exception as error:
      print(error.to_dict())
      return error.client_view()
  if request.method == 'POST':
    try:
      return create_user(
        name=request.form['name'], 
        email=request.form['email'], 
        bio=request.form['bio']
      )
    except Exception as error:
      print(error.to_dict())
      return error.client_view()


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_show_update_delete(id):
  if request.method == 'GET':
    try:
      return get_user(id)
    except Exception as error:
      print(error.to_dict())
      return error.client_view()
  if request.method == 'PUT':
    try:
      return update_user(
        id=id, 
        name=request.form['name'],
        email=request.form['email'],
        bio=request.form['bio']
      )
    except Exception as error:
      print(error.to_dict())
      return error.client_view()
  if request.method == 'DELETE':
    try:
      return destroy_user(id)
    except Exception as error:
      print(error.to_dict())
      return error.client_view()