from flask import jsonify, request
# Helper Functions
def error(err_locale, err):
  print(f'💩 Fucking Yikes bud, there was an error in {err_locale}\n{err}')
  return jsonify(error='Server Error')

from models import app, User
from crud.user_crud import get_all_users, get_user

# Routes
@app.route('/users')
def user_index_create():
  try:
    return get_all_users()
  except Exception as err:
    return error('user index route', err)

@app.route('/users/<int:id>')
def user_show_put_delete(id):
  try:
    return get_user(id)
  except Exception as err:
    return error('the GET /users/:id route', err)

# @app.route('/testjson', methods=["POST"])
# def json_test():
#   print(f'🌡 {request}')
#   return jsonify(messge='poop')

