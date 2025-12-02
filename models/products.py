import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Products(db.Model):
  __tablename__ = 'Products'

  product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Companies.company_id'), nullable=False)
  company_name = db.Column(db.String(), nullable=False, unique=True)
  price = db.Column(db.Integer())
  description = db.Column(db.String())
  active = db.Column(db.Boolean(), nullable=False, default=True)

  company = db.relationship("Companies", back_populates="products")
  warranty = db.relationship("Warranties", back_populates="product", uselist=False, cascade="all, delete-orphan")
  categories = db.relationship("ProductsCategoriesXref", back_populates="product", cascade="all, delete-orphan")

  def __init__(self, company_id, company_name, price=None, description=None, active=True):
    self.company_id = company_id
    self.company_name = company_name
    self.price = price
    self.description = description
    self.active = active

  def new_product_obj():
    return Products('', '', None, None, True)


class ProductSchema(ma.Schema):
  class Meta:
    fields = ['product_id', 'company_id', 'company_name', 'price', 'description', 'active', 'warranty', 'categories']

  product_id = ma.fields.UUID()
  company_id = ma.fields.UUID(required=True)
  company_name = ma.fields.String(required=True)
  price = ma.fields.Integer(allow_none=True)
  description = ma.fields.String(allow_none=True)
  active = ma.fields.Boolean(required=True, dump_default=True)

  warranty = ma.fields.Nested("WarrantySchema", exclude=['product'])
  categories = ma.fields.Nested("ProductsCategoriesXrefSchema", many=True, exclude=['product'])


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)