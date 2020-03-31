from flask import jsonify, redirect
from models import db, User

def error(err_locale, error):
  print(f'💩 Error in {err_locale}\n{error}')
  return jsonify(error='Server Error')

# Index
def get_all_users():
  try:
    all_users = User.query.all()
    results = [user.as_dict() for user in all_users]
    return jsonify(results)
  except Exception as error:
    return error('getting all users', error)

# Show
def get_user(id):
  try:
    user = User.query.get(id)
    print(user)
    if user:
      return jsonify(user.as_dict())
    else:
      raise Exception('No user at that id')
  except Exception as error:
    return error('getting one user', error)

# Create
def create_user(name, email, bio):
  try:
    new_user = User(name=name, email=email, bio=bio or None)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict())
  except Exception as error:
    return error('creating a user', error)

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
      # return error('updating one user', 'No user at that id')
      return jsonify(message="no user here")
  except Exception as error:
    return error('updating a user', error)

# Destroy
def destroy_user(id):
  try:
    user = User.query.get(id)
    if user:
      db.session.delete(user)
      db.session.commit()
      return redirect('/users')
    else:
      return error('deleting one user', 'No user at that id')
  except Exception as error:
    return error('deleting a user', error)