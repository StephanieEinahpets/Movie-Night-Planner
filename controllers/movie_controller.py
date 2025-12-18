from flask import jsonify, request

from db import db
from models.movies import Movies, movie_schema, movies_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


@authenticate_return_auth
def add_movie(auth_info):
  post_data = request.form if request.form else request.json
  
  new_movie = Movies.new_movie_obj()
  populate_object(new_movie, post_data)
  
  if not new_movie.recommender_id:
    new_movie.recommender_id = auth_info.user.user_id

  try:
    db.session.add(new_movie)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to add movie"}), 400
  
  return jsonify({"message": "movie added", "result": movie_schema.dump(new_movie)}), 201


def get_all_movies():
  movie_query = db.session.query(Movies).all()
  
  if not movie_query:
    return jsonify({"message": "no movies found"}), 404
  
  return jsonify({"message": "movies found", "results": movies_schema.dump(movie_query)}), 200


def get_movie_by_id(movie_id):
  movie_query = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
  
  if not movie_query:
    return jsonify({"message": "movie not found"}), 404
  
  return jsonify({"message": "movie found", "result": movie_schema.dump(movie_query)}), 200


@authenticate_return_auth
def update_movie_by_id(movie_id, auth_info):
  movie_query = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
  
  if not movie_query:
    return jsonify({"message": "movie not found"}), 404

  if auth_info.user.role != 'admin' and movie_query.recommender_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only update own movies"}), 403

  put_data = request.form if request.form else request.json
  populate_object(movie_query, put_data)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to update movie"}), 400

  return jsonify({"message": "movie updated", "result": movie_schema.dump(movie_query)}), 200


@authenticate_return_auth
def delete_movie(auth_info):
  post_data = request.form if request.form else request.json
  movie_id = post_data.get('movie_id')

  movie_query = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

  if not movie_query:
    return jsonify({"message": "movie not found"}), 404

  if auth_info.user.role != 'admin' and movie_query.recommender_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only delete own movies"}), 403

  try:
    db.session.delete(movie_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to delete movie"}), 400

  return jsonify({"message": "movie deleted", "result": movie_schema.dump(movie_query)}), 200