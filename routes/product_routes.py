from flask import Blueprint

import controllers

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def add_product_route():
  return controllers.add_product()

@products.route('/products', methods=['GET'])
def get_all_products_route():
  return controllers.get_all_products()

@products.route('/products/active', methods=['GET'])
def get_all_active_products_route():
  return controllers.get_all_active_products()

@products.route('/product/<product_id>', methods=['GET'])
def get_product_by_id_route(product_id):
  return controllers.get_product_by_id(product_id)

@products.route('/product/company/<company_id>', methods=['GET'])
def get_products_by_company_id_route(company_id):
  return controllers.get_products_by_company_id(company_id)

@products.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id_route(product_id):
  return controllers.update_product_by_id(product_id)

@products.route('/product/delete', methods=['DELETE'])
def delete_product_route():
  return controllers.delete_product()

@products.route('/product/category', methods=['POST'])
def add_product_category_association_route():
  return controllers.add_product_category_association()