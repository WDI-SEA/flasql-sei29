from flask import jsonify, redirect
from models import db, User

# Index
def get_all_users():
  all_users = User.query.all()
  if len(all_users) > 0:
    results = [user.as_dict() for user in all_users]
  else:
    results = []
  return jsonify(results)

# Show
def get_user(id):
  user = User.query.get(id)
  if user:
    return jsonify(user.as_dict())
  else:
    raise Exception('No User at id {}'.format(id))

# Create
def create_user(name, email, bio):
  new_user = User(name=name, email=email, bio=bio or None)
  db.session.add(new_user)
  db.session.commit()
  return jsonify(new_user.as_dict())

# Update function!
def update_user(id, name, email, bio):
  user = User.query.get(id)
  if user:
    user.email = email or user.email
    user.name = name or user.name
    user.bio = bio or user.bio
    db.session.commit()
    return jsonify(user.as_dict())
  else:
    raise Exception('No User at id {}'.format(id))

# Destroy
def destroy_user(id):
  user = User.query.get(id)
  if user:
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
  else:
    raise Exception('No User at id {}'.format(id))