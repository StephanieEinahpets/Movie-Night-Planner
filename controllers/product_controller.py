from flask import jsonify, request

from db import db
from models.products import Products, product_schema, products_schema
from models.companies import Companies
from models.products_categories_xref import ProductsCategoriesXref, xref_schema
from models.warranties import Warranties
from models.categories import Categories
from util.reflection import populate_object
from lib.authenticate import authenticate


@authenticate
def add_product():
  post_data = request.form if request.form else request.json
  company_id = post_data.get('company_id')
  new_product = Products.new_product_obj()
  populate_object(new_product, post_data)

  if company_id:
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company_query == None:
      return jsonify({"message": "company_id is required"}), 400

  try:
    db.session.add(new_product)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add record"}), 400

  return jsonify({"message": "product added", "result": product_schema.dump(new_product)}), 201


@authenticate
def get_all_products():
  products_query = db.session.query(Products).all()
  return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def get_all_active_products():
  products_query = db.session.query(Products).filter(Products.active == True).all()
  return jsonify({"message": "active products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def get_product_by_id(product_id):
  product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
  
  if not product_query:
    return jsonify({"message": "product not found"}), 404
  
  return jsonify({"message": "product found", "result": product_schema.dump(product_query)}), 200


@authenticate
def get_products_by_company_id(company_id):
  products_query = db.session.query(Products).filter(Products.company_id == company_id).all()
  return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def update_product_by_id(product_id):
  product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
  
  if not product_query:
    return jsonify({"message": "product not found"}), 404

  put_data = request.form if request.form else request.json
  populate_object(product_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update record"}), 400

  return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200


@authenticate
def delete_product():
  post_data = request.form if request.form else request.json
  product_id = post_data.get('product_id')

  product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

  if not product_query:
    return jsonify({"message": "product not found"}), 404

  db.session.query(ProductsCategoriesXref).filter(ProductsCategoriesXref.product_id == product_id).delete()
  db.session.query(Warranties).filter(Warranties.product_id == product_id).delete()

  try:
    db.session.delete(product_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete record"}), 400

  return jsonify({"message": "product deleted", "result": product_schema.dump(product_query)}), 200


@authenticate
def add_product_category_association():
  post_data = request.form if request.form else request.json
  product_id = post_data.get('product_id')
  category_id = post_data.get('category_id')

  if not product_id or not category_id:
    return jsonify({"message": "product_id and category_id are required"}), 400

  product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
  if not product_query:
    return jsonify({"message": "product not found"}), 404

  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
  if not category_query:
    return jsonify({"message": "category not found"}), 404

  existing_xref = db.session.query(ProductsCategoriesXref).filter(
    ProductsCategoriesXref.product_id == product_id,
    ProductsCategoriesXref.category_id == category_id
  ).first()

  if existing_xref:
    return jsonify({"message": "association already exists"}), 400

  new_xref = ProductsCategoriesXref(product_id, category_id)

  try:
    db.session.add(new_xref)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add record"}), 400

  return jsonify({"message": "product-category association added", "result": xref_schema.dump(new_xref)}), 201