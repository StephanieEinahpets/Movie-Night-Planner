from flask import Blueprint

import controllers

movies = Blueprint('movies', __name__)

@movies.route('/movie', methods=['POST'])
def add_movie_route():
  return controllers.add_movie()

@movies.route('/movies', methods=['GET'])
def get_all_movies_route():
  return controllers.get_all_movies()

@movies.route('/movie/<movie_id>', methods=['GET'])
def get_movie_by_id_route(movie_id):
  return controllers.get_movie_by_id(movie_id)

@movies.route('/movie/<movie_id>', methods=['PUT'])
def update_movie_by_id_route(movie_id):
  return controllers.update_movie_by_id(movie_id)

@movies.route('/movie/delete', methods=['DELETE'])
def delete_movie_route():
  return controllers.delete_movie()