from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def add_user():
  post_data = request.form if request.form else request.json
  
  new_user = AppUsers.new_user_obj()
  populate_object(new_user, post_data)

  if new_user.password:
    new_user.password = generate_password_hash(new_user.password).decode('utf8')
  else:
    return jsonify({"message": "password is required"}), 400

  try:
    db.session.add(new_user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to add user - email or username may already exist"}), 400
  
  return jsonify({"message": "user added", "result": app_user_schema.dump(new_user)}), 201


@authenticate_return_auth
def get_all_users(auth_info):
  if auth_info.user.role != 'admin':
    return jsonify({"message": "unauthorized - admin only"}), 403
  
  user_query = db.session.query(AppUsers).all()
  
  if not user_query:
    return jsonify({"message": "no users found"}), 404
  
  return jsonify({"message": "users found", "results": app_users_schema.dump(user_query)}), 200


@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
  user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  
  if not user_query:
    return jsonify({"message": "user not found"}), 404
  
  if auth_info.user.role == 'admin' or user_id == str(auth_info.user.user_id):
    return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200
  
  return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
  user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  
  if not user_query:
    return jsonify({"message": "user not found"}), 404

  if auth_info.user.role != 'admin' and user_id != str(auth_info.user.user_id):
    return jsonify({"message": "unauthorized - can only update own record"}), 403

  put_data = request.form if request.form else request.json
  
  if 'password' in put_data:
    put_data['password'] = generate_password_hash(put_data['password']).decode('utf8')
  
  populate_object(user_query, put_data)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to update user"}), 400

  return jsonify({"message": "user updated", "result": app_user_schema.dump(user_query)}), 200


@authenticate_return_auth
def delete_user(auth_info):
  if auth_info.user.role != 'admin':
    return jsonify({"message": "unauthorized - admin only"}), 403
  
  post_data = request.form if request.form else request.json
  user_id = post_data.get('user_id')

  if not user_id:
    return jsonify({"message": "user_id is required"}), 400

  user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": "user not found"}), 404

  try:
    db.session.delete(user_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to delete user"}), 400

  return jsonify({"message": "user deleted", "result": app_user_schema.dump(user_query)}), 200