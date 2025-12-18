from flask import Blueprint

import controllers

movieimages = Blueprint('movieimages', __name__)


@movieimages.route('/movieimage', methods=['POST'])
def add_movie_image_route():
  return controllers.add_movie_image()

@movieimages.route('/movieimages', methods=['GET'])
def get_all_movie_images_route():
  return controllers.get_all_movie_images()

@movieimages.route('/movieimage/<movie_image_id>', methods=['GET'])
def get_movie_image_by_id_route(movie_image_id):
  return controllers.get_movie_image_by_id(movie_image_id)

@movieimages.route('/movieimage/<movie_image_id>', methods=['PUT'])
def update_movie_image_by_id_route(movie_image_id):
  return controllers.update_movie_image_by_id(movie_image_id)

@movieimages.route('/movieimage/delete', methods=['DELETE'])
def delete_movie_image_route():
  return controllers.delete_movie_image()