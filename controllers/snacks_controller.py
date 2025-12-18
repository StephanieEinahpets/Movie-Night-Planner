from flask import jsonify, request

from db import db
from models.snacks import Snacks, snack_schema, snacks_schema
from models.movie_nights import MovieNights
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate_return_auth
def add_snack(auth_info):
  post_data = request.form if request.form else request.json
  movie_night_id = post_data.get('movie_night_id')
  
  if not movie_night_id:
    return jsonify({"message": "movie_night_id is required"}), 400
  
  movie_night_query = db.session.query(MovieNights).filter(MovieNights.movie_night_id == movie_night_id).first()
  if not movie_night_query:
    return jsonify({"message": "movie night not found"}), 404
  
  new_snack = Snacks.new_snack_obj()
  populate_object(new_snack, post_data)
  
  if not new_snack.user_id:
    new_snack.user_id = auth_info.user.user_id

  try:
    db.session.add(new_snack)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add snack"}), 400
  
  return jsonify({"message": "snack added", "result": snack_schema.dump(new_snack)}), 201


@authenticate
def get_all_snacks():
  snack_query = db.session.query(Snacks).all()
  
  if not snack_query:
    return jsonify({"message": "no snacks found"}), 404
  
  return jsonify({"message": "snacks found", "results": snacks_schema.dump(snack_query)}), 200


@authenticate
def get_snack_by_id(snack_id):
  snack_query = db.session.query(Snacks).filter(Snacks.snack_id == snack_id).first()
  
  if not snack_query:
    return jsonify({"message": "snack not found"}), 404
  
  return jsonify({"message": "snack found", "result": snack_schema.dump(snack_query)}), 200


@authenticate_return_auth
def update_snack_by_id(snack_id, auth_info):
  snack_query = db.session.query(Snacks).filter(Snacks.snack_id == snack_id).first()
  
  if not snack_query:
    return jsonify({"message": "snack not found"}), 404

  if auth_info.user.role != 'admin' and snack_query.user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only update own snacks"}), 403

  put_data = request.form if request.form else request.json
  populate_object(snack_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update snack"}), 400

  return jsonify({"message": "snack updated", "result": snack_schema.dump(snack_query)}), 200


@authenticate_return_auth
def delete_snack(auth_info):
  post_data = request.form if request.form else request.json
  snack_id = post_data.get('snack_id')

  snack_query = db.session.query(Snacks).filter(Snacks.snack_id == snack_id).first()

  if not snack_query:
    return jsonify({"message": "snack not found"}), 404

  if auth_info.user.role != 'admin' and snack_query.user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only delete own snacks"}), 403

  try:
    db.session.delete(snack_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete snack"}), 400

  return jsonify({"message": "snack deleted", "result": snack_schema.dump(snack_query)}), 200