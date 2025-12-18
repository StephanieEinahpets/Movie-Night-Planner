from flask import jsonify, request

from db import db
from models.movie_images import MovieImages, movie_image_schema, movie_images_schema
from models.movies import Movies
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


@authenticate_return_auth
def add_movie_image(auth_info):
  post_data = request.form if request.form else request.json

  if not post_data.get('movie_id'):
    return jsonify({"message": "movie_id is required"}), 400

  movie = db.session.query(Movies).filter(Movies.movie_id == post_data['movie_id']).first()

  if not movie:
    return jsonify({"message": "movie not found"}), 404

  if movie.movie_image:
    return jsonify({"message": "movie already has an image"}), 400

  new_image = MovieImages.new_movie_image_obj()
  populate_object(new_image, post_data)

  try:
    db.session.add(new_image)
    db.session.commit()
  except Exception:
    db.session.rollback()
    return jsonify({"message": "unable to add movie image"}), 400

  return jsonify({"message": "movie image added", "result": movie_image_schema.dump(new_image)}), 201


def get_all_movie_images():
  movie_image_query = db.session.query(MovieImages).all()
  
  if not movie_image_query:
    return jsonify({"message": "no movie images found"}), 404
  
  return jsonify({"message": "movie images found", "results": movie_images_schema.dump(movie_image_query)}), 200


def get_movie_image_by_id(movie_image_id):
  image = db.session.query(MovieImages).filter(MovieImages.movie_image_id == movie_image_id).first()
  if not image:
    return jsonify({"message": "movie image not found"}), 404

  return jsonify({"message": "movie image found", "result": movie_image_schema.dump(image)}), 200


def get_movie_image_by_movie_id(movie_id):
  image = db.session.query(MovieImages).filter(MovieImages.movie_id == movie_id).first()
  if not image:
    return jsonify({"message": "movie image not found"}), 404

  return jsonify({"message": "movie image found", "result": movie_image_schema.dump(image)}), 200



@authenticate_return_auth
def update_movie_image(movie_image_id, auth_info):
  image = db.session.query(MovieImages).filter(MovieImages.movie_image_id == movie_image_id).first()
  if not image:
    return jsonify({"message": "movie image not found"}), 404

  movie = image.movie
  if auth_info.user.role != 'admin' and movie.recommender_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized"}), 403

  put_data = request.form if request.form else request.json
  populate_object(image, put_data)

  try:
    db.session.commit()
  except Exception:
    db.session.rollback()
    return jsonify({"message": "unable to update movie image"}), 400

  return jsonify({"message": "movie image updated", "result": movie_image_schema.dump(image)}), 200


@authenticate_return_auth
def delete_movie_image(movie_image_id, auth_info):
  image = db.session.query(MovieImages).filter(MovieImages.movie_image_id == movie_image_id).first()
  if not image:
    return jsonify({"message": "movie image not found"}), 404

  movie = image.movie
  if auth_info.user.role != 'admin' and movie.recommender_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized"}), 403

  try:
    db.session.delete(image)
    db.session.commit()
  except Exception:
    db.session.rollback()
    return jsonify({"message": "unable to delete movie image"}), 400

  return jsonify({"message": "movie image deleted", "result": movie_image_schema.dump(image)}), 200