import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Companies(db.Model):
  __tablename__ = 'Companies'
  
  company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  company_name = db.Column(db.String(), nullable=False, unique=True)
  users = db.relationship("AppUsers", back_populates="company")
  products = db.relationship("Products", back_populates="company", cascade="all, delete-orphan")

  def __init__(self, company_name):
    self.company_name = company_name

  def new_company_obj():
    return Companies('')


class CompanySchema(ma.Schema):
  class Meta:
    fields = ['company_id', 'company_name']

  company_id = ma.fields.UUID()
  company_name = ma.fields.String(required=True)


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)