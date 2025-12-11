from flask import jsonify, request

from db import db
from models.categories import Categories, category_schema, categories_schema
from models.products_categories_xref import ProductsCategoriesXref
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def add_category():
  post_data = request.form if request.form else request.json

  new_category = Categories.new_category_obj()
  populate_object(new_category, post_data)

  try:
    db.session.add(new_category)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add record"}), 400

  return jsonify({"message": "category added", "result": category_schema.dump(new_category)}), 201


@authenticate_return_auth
def get_all_categories():
  categories_query = db.session.query(Categories).all()
  return jsonify({"message": "categories found", "results": categories_schema.dump(categories_query)}), 200


@authenticate_return_auth
def get_category_by_id(category_id):
  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
  
  if not category_query:
    return jsonify({"message": "category not found"}), 404
  
  return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def update_category_by_id(category_id):
  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
  
  if not category_query:
    return jsonify({"message": "category not found"}), 404

  put_data = request.form if request.form else request.json
  populate_object(category_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update record"}), 400

  return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def delete_category(auth_info):
  if auth_info.user.role != 'admin':
    return jsonify({"message": "unauthorized - admin only"}), 403

  post_data = request.form if request.form else request.json
  category_id = post_data.get('category_id')
  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

  if not category_query:
    return jsonify({"message": "category not found"}), 404

  db.session.query(ProductsCategoriesXref).filter(ProductsCategoriesXref.category_id == category_id).delete()

  try:
    db.session.delete(category_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete record"}), 400

  return jsonify({"message": "category deleted", "result": category_schema.dump(category_query)}), 200