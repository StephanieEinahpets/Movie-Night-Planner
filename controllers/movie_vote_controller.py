from flask import jsonify, request
import json

from db import db
from models.movie_votes import MovieVotes, movie_vote_schema, movie_votes_schema
from models.movies import Movies, movie_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate_return_auth
def add_vote_to_movie(auth_info):
  post_data = request.form if request.form else request.json

  movie_id = post_data.get("movie_id")
  voted_for = post_data.get("voted_for")

  if not movie_id:
    return jsonify({"message": "movie_id is required"}), 400
  if voted_for is None:
    return jsonify({"message": "voted_for is required"}), 400

  if isinstance(voted_for, str):
    voted_for = voted_for.lower() == "true"

  movie = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
  if not movie:
    return jsonify({"message": "movie not found"}), 404

  new_vote = MovieVotes(
    user_id=auth_info.user.user_id,
    voted_for=voted_for
  )

  try:
    db.session.add(new_vote)
    db.session.flush()
    new_vote.movies.append(movie)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to add movie vote", "error": str(e)}), 400

  return jsonify(
    {"message": "vote added to movie", "result": movie_vote_schema.dump(new_vote)}
  ), 201

@authenticate
def get_movie_vote_by_id(movie_vote_id):
  movie_vote_query = db.session.query(MovieVotes).filter(MovieVotes.movie_vote_id == movie_vote_id).first()
  
  if not movie_vote_query:
    return jsonify({"message": "movie vote not found"}), 404
  
  return jsonify({"message": "movie vote found", "result": movie_vote_schema.dump(movie_vote_query)}), 200

@authenticate
def get_all_movie_votes():
  movie_vote_query = db.session.query(MovieVotes).all()

  if not movie_vote_query:
    return jsonify({"message": "no movie votes found"}), 404

  return jsonify(
    {
      "message": "movie votes found",
      "results": movie_votes_schema.dump(movie_vote_query)
    }
  ), 200

@authenticate_return_auth
def update_movie_vote_by_id(movie_vote_id, auth_info):
  movie_vote_query = db.session.query(MovieVotes).filter(MovieVotes.movie_vote_id == movie_vote_id).first()

  if not movie_vote_query:
    return jsonify({"message": "movie vote not found"}), 404

  if auth_info.user.role != 'admin' and movie_vote_query.user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only update own votes"}), 403

  put_data = request.form if request.form else request.json
  populate_object(movie_vote_query, put_data)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to update movie vote", "error": str(e)}), 400

  return jsonify({"message": "movie vote updated", "result": movie_vote_schema.dump(movie_vote_query)}), 200



@authenticate_return_auth
def delete_movie_vote(auth_info):
  post_data = request.form if request.form else request.json
  movie_vote_id = post_data.get('movie_vote_id')

  movie_vote_query = db.session.query(MovieVotes).filter(MovieVotes.movie_vote_id == movie_vote_id).first()

  if not movie_vote_query:
    return jsonify({"message": "movie vote not found"}), 404

  if auth_info.user.role != 'admin' and movie_vote_query.user_id != auth_info.user.user_id:
    return jsonify({"message": "unauthorized - can only delete own votes"}), 403

  try:
    db.session.delete(movie_vote_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "unable to delete movie vote", "error": str(e)}), 400

  return jsonify({"message": "movie vote deleted", "result": movie_vote_schema.dump(movie_vote_query)}), 200
