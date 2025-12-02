from flask import jsonify, request

from db import db
from models.warranties import Warranties, warranty_schema
from models.products import Products
from util.reflection import populate_object
from lib.authenticate import authenticate


@authenticate
def add_warranty():
  post_data = request.form if request.form else request.json
  product_id = post_data.get('product_id')
  new_warranty = Warranties.new_warranty_obj()
  populate_object(new_warranty, post_data)

  if product_id:
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_query == None:
      return jsonify({"message": "product_id is required"}), 400

  try:
    db.session.add(new_warranty)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to add record"}), 400

  return jsonify({"message": "warranty added", "result": warranty_schema.dump(new_warranty)}), 201


@authenticate
def get_warranty_by_id(warranty_id):
  warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
  
  if not warranty_query:
    return jsonify({"message": "warranty not found"}), 404
  
  return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200


@authenticate
def update_warranty_by_id(warranty_id):
  warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
  
  if not warranty_query:
    return jsonify({"message": "warranty not found"}), 404

  put_data = request.form if request.form else request.json
  populate_object(warranty_query, put_data)

  try:
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to update record"}), 400

  return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200


@authenticate
def delete_warranty():
  post_data = request.form if request.form else request.json
  warranty_id = post_data.get('warranty_id')

  warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

  if not warranty_query:
    return jsonify({"message": "warranty not found"}), 404

  try:
    db.session.delete(warranty_query)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete record"}), 400

  return jsonify({"message": "warranty deleted", "result": warranty_schema.dump(warranty_query)}), 200