import json
from flask import jsonify, redirect
from models import db, get_or_create, User, Post, Tag

def get_all_posts():
  all_posts = Post.query.all()
  if len(all_posts) > 0:
    result = [post.as_dict() for post in all_posts]
    return jsonify(result)
  else: 
    raise Exception('No Posts Found')

def get_post(id):
  post = Post.query.get(id)
  if post:
    most_post = post.as_dict()
    most_post['author'] = post.author.as_dict()
    most_post['tags'] = [tag.as_dict() for tag in post.tags]
    return jsonify(most_post)
  else:
    raise Exception('Error getting post at {}'.format(id))

def create_post(tags, **post_kwargs):
  new_post = Post(**post_kwargs)
  # Assuming tags is a list of strings
  new_post.tags = [get_or_create(Tag, tag=tag)[0] for tag in tags]
  db.session.add(new_post)
  db.session.commit()
  return jsonify(new_post.as_dict())

def update_post(id, **form_kwargs):
  post = Post.query.get(id)
  if post:
    for k, v in form_kwargs.items():
      if k == 'tags':
        v = [get_or_create(Tag, tag=tag)[0] for tag in v]
      setattr(post, k, v)
    db.session.commit()
    return redirect(f'/posts/{id}')
  else:
    raise Exception('Error updating post at {}'.format(id))

def destroy_post(id):
  post = Post.query.get(id)
  if post:
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
  else:
    raise Exception('Error destroying post at {}'.format(id))