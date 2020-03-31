from flask import jsonify, redirect
from models import db, User
from api import error

def get_all_users():
  try:
    all_users = User.query.all()
    results = [user.as_dict() for user in all_users] 
    return jsonify(results)
  except Exception as err: 
    return error('getting all users', err)

def get_user(id):
  try:
    user = User.query.get(id)
    if user:
      return jsonify(user.as_dict())
    else:
      raise Exception('Error getting user at {}'.format(id))
  except Exception as err:
      return error('getting one user', err)