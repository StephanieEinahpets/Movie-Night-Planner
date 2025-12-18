from flask import Blueprint

import controllers

snacks = Blueprint('snacks', __name__)

@snacks.route('/snack', methods=['POST'])
def add_snack_route():
  return controllers.add_snack()

@snacks.route('/snacks', methods=['GET'])
def get_all_snacks_route():
  return controllers.get_all_snacks()

@snacks.route('/snack/<snack_id>', methods=['GET'])
def get_snack_by_id_route(snack_id):
  return controllers.get_snack_by_id(snack_id)

@snacks.route('/snack/<snack_id>', methods=['PUT'])
def update_snack_by_id_route(snack_id):
  return controllers.update_snack_by_id(snack_id)

@snacks.route('/snack/delete', methods=['DELETE'])
def delete_snack_route():
  return controllers.delete_snack()