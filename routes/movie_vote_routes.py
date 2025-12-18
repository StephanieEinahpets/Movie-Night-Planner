from flask import Blueprint

import controllers

movievotes = Blueprint('movievotes', __name__)


@movievotes.route('/movievote', methods=['POST'])
def add_vote_to_movies_route():
  return controllers.add_movie_vote()

@movievotes.route('/movievotes', methods=['GET'])
def get_all_movie_votes_route():
  return controllers.get_all_movie_votes()

@movievotes.route('/movievote/<movie_vote_id>', methods=['GET'])
def get_movie_vote_by_id_route(movie_vote_id):
  return controllers.get_movie_vote_by_id(movie_vote_id)

@movievotes.route('/movievote/<movie_vote_id>', methods=['PUT'])
def update_movie_vote_by_id_route(movie_vote_id):
  return controllers.update_movie_vote_by_id(movie_vote_id)

@movievotes.route('/movievote/delete', methods=['DELETE'])
def delete_movie_vote_route():
  return controllers.delete_movie_vote()

