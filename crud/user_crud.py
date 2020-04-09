from flask import jsonify, redirect, g
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
def create_user(**form_args):
  if not form_args['name'] or not form_args['email'] or not form_args['password']:
    raise Exception('Name, email, and password are required fields')
  if User.query.filter_by(name=form_args['name']).first() is not None:
    raise Exception('There is already a user with this email')

  new_user = User(**form_args)
  new_user.set_password(form_args['password'])
  db.session.add(new_user)
  db.session.commit()
  # Authorize the user
  token = new_user.generate_token()
  return jsonify(user=new_user.as_dict(), token=token.decode('ascii'), status_code=201)

# Update function!
def update_user(id, **update_values):
  user = User.query.get(id)
  if user and user.id == g.user.id:
    for key, value in update_values.items():
      setattr(user, key, value)
    db.session.commit()
    return jsonify(user.as_dict())
  else:
    raise Exception('Error updating user at id {}'.format(id))

# Destroy
def destroy_user(id):
  user = User.query.get(id)
  if user and user.id == g.user.id:
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
  else:
    raise Exception('Error Destroying User at id {}'.format(id))