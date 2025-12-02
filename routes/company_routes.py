from flask import Blueprint

import controllers

companies = Blueprint('companies', __name__)


@companies.route('/company', methods=['POST'])
def add_company_route():
  return controllers.add_company()

@companies.route('/companies', methods=['GET'])
def get_all_companies_route():
  return controllers.get_all_companies()

@companies.route('/company/<company_id>', methods=['GET'])
def get_company_by_id_route(company_id):
  return controllers.get_company_by_id(company_id)

@companies.route('/company/<company_id>', methods=['PUT'])
def update_company_by_id_route(company_id):
  return controllers.update_company_by_id(company_id)

@companies.route('/company/delete', methods=['DELETE'])
def delete_company_route():
  return controllers.delete_company()