from flask import jsonify, request

from db import db
from models.movie_nights import MovieNights, movie_night_schema, movie_nights_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate_return_auth
def add_movie_night(auth_info):
  post_data = request.form if request.form else request.json
  
  new_movie_night = MovieNights.new_movie_night_obj()
  populate_object(new_movie_night, post_data)
  
  if not new_movie_night.host_user_id:
    new_movie_night.host_user_id = auth_info.user.user_id

  try:
    db.session.add(new_movie_night)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add movie night"}), 400
  
  return jsonify({"message": "movie night added", "result": movie_night_schema.dump(new_movie_night)}), 201


@authenticate
def get_all_movie_nights():
  movie_night_query = db.session.query(MovieNights).all()
  
  if not movie_night_query:
    return jsonify({"message": "no movie nights found"}), 404
  
  return jsonify({"message": "movie nights found", "results": movie_nights_schema.dump(movie_night_query)}), 200


@authenticate
def get_movie_night_by_id(movie_night_id):
  movie_night_query = db.session.query(MovieNights).filter(MovieNights.movie_night_id == movie_night_id).first()
  
  if not movie_night_query:
    return jsonify({"message": "movie night not found"}), 404
  
  return jsonify({"message": "movie night found", "result": movie_night_schema.dump(movie_night_query)}), 200


@authenticate_return_auth
def update_movie_night_by_id(movie_night_id, auth_info):
  movie_night_query = db.session.query(MovieNights).filter(MovieNights.movie_night_id == movie_night_id).first()
  
  if not movie_night_query:
    return jsonify({"message": "movie night not found"}), 404

  if auth_info.user.role != 'admin' and movie_night_query.host_user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only update own movie nights"}), 403

  put_data = request.form if request.form else request.json
  populate_object(movie_night_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update movie night"}), 400

  return jsonify({"message": "movie night updated", "result": movie_night_schema.dump(movie_night_query)}), 200


@authenticate_return_auth
def delete_movie_night(auth_info):
  post_data = request.form if request.form else request.json
  movie_night_id = post_data.get('movie_night_id')

  if not movie_night_id:
    return jsonify({"message": "movie_night_id is required"}), 400

  movie_night_query = db.session.query(MovieNights).filter(MovieNights.movie_night_id == movie_night_id).first()
  if not movie_night_query:
    return jsonify({"message": "movie night not found"}), 404

  if auth_info.user.role != 'admin' and movie_night_query.host_user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only delete own movie nights"}), 403

  result = movie_night_schema.dump(movie_night_query)

  try:
    db.session.delete(movie_night_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete movie night"}), 400

  return jsonify({"message": "movie night deleted", "result": result}), 200