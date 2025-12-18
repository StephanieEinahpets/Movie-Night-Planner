from flask import jsonify, request

from db import db
from models.app_users import AppUsers, app_users_schema
from lib.authenticate import authenticate_return_auth

@authenticate_return_auth
def users_get_by_search():
  search_term = request.args.get('q').lower()
  user_data = db.session.query(AppUsers).filter(db.or_(db.func.lower(AppUsers.username).contains(search_term), db.func.lower(AppUsers.email).contains(search_term))).order_by(AppUsers.last_name.asc()).all()
  return jsonify({"message": "users found", "results": app_users_schema.dump(user_data)}), 200