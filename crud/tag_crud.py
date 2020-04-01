import json
from flask import jsonify, redirect
from models import db, get_or_create, Post, Tag

def get_all_tags():
  tags = Tag.query.all()
  if len(tags) > 0:
    return jsonify([tag.as_dict() for tag in tags])
  else:
    raise Exception('Error getting all tags')

def get_posts_by_tag(id):
  tag = Tag.query.get(id)
  if tag:
    return jsonify(tag=tag.as_dict(), posts=[post.as_dict() for post in tag.posts])
  else: 
    raise Exception(f'No Tag Found at id {id}')

def destroy_tag(id):
  tag = Tag.query.get(id)
  if tag:
    db.session.delete(tag)
    print(tag.tag)
    # db.session.commit()
    return jsonify(message='Successfully deleted tag', status_code=200)
  else:
    raise Exception('Error destroying tag at {}'.format(id))