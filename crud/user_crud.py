from flask import jsonify, redirect
from helpers import InvalidUsage
from models import db, User

# Index
def get_all_users():
  try:
    all_users = User.query.all()
    results = [user.as_dict() for user in all_users]
    return jsonify(results)
  except Exception as error:
    print(error.to_dict())
    return error.client_view()

# Show
def get_user(id):
  try:
    user = User.query.get(id)
    print(user)
    if user:
      return jsonify(user.as_dict())
    else:
      raise InvalidUsage('No user at that id')
  except Exception as error:
    print(error.to_dict())
    return error.client_view()

# Create
def create_user(name, email, bio):
  try:
    new_user = User(name=name, email=email, bio=bio or None)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict())
  except Exception as error:
    print(error.to_dict())
    return error.client_view()

# Update function!
def update_user(id, name, email, bio):
  try:
    user = User.query.get(id)
    if user:
      user.email = email or user.email
      user.name = name or user.name
      user.bio = bio or user.bio
      db.session.commit()
      return jsonify(user.as_dict())
      # return redirect(f'/users/{id}')
    else:
      # return jsonify(error.to_dict())
      raise InvalidUsage('No User here!')
  except Exception as error:
    print(error.to_dict())
    return error.client_view()

# Destroy
def destroy_user(id):
  try:
    user = User.query.get(id)
    if user:
      db.session.delete(user)
      db.session.commit()
      return redirect('/users')
    else:
      raise InvalidUsage('No user here')
  except Exception as error:
    print(error.to_dict())
    return error.client_view()