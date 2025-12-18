from flask import Blueprint

import controllers

movienights = Blueprint('movienights', __name__)


@movienights.route('/movienight', methods=['POST'])
def add_movie_night_route():
  return controllers.add_movie_night()

@movienights.route('/movienights', methods=['GET'])
def get_all_movie_nights_route():
  return controllers.get_all_movie_nights()

@movienights.route('/movienight/<movie_night_id>', methods=['GET'])
def get_movie_night_by_id_route(movie_night_id):
  return controllers.get_movie_night_by_id(movie_night_id)

@movienights.route('/movienight/<movie_night_id>', methods=['PUT'])
def update_movie_night_by_id_route(movie_night_id):
  return controllers.update_movie_night_by_id(movie_night_id)

@movienights.route('/movienight/delete', methods=['DELETE'])
def delete_movie_night_route():
  return controllers.delete_movie_night()