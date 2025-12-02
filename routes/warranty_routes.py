from flask import Blueprint

import controllers

warranties = Blueprint('warranties', __name__)


@warranties.route('/warranty', methods=['POST'])
def add_warranty_route():
  return controllers.add_warranty()


@warranties.route('/warranty/<warranty_id>', methods=['GET'])
def get_warranty_by_id_route(warranty_id):
    return controllers.get_warranty_by_id(warranty_id)


@warranties.route('/warranty/<warranty_id>', methods=['PUT'])
def update_warranty_by_id_route(warranty_id):
  return controllers.update_warranty_by_id(warranty_id)


@warranties.route('/warranty/delete', methods=['DELETE'])
def delete_warranty_route():
  return controllers.delete_warranty()