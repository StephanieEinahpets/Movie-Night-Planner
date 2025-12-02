import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class ProductsCategoriesXref(db.Model):
  __tablename__ = 'ProductsCategoriesXref'

  product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Products.product_id'), primary_key=True)
  category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Categories.category_id'), primary_key=True)

  product = db.relationship("Products", back_populates="categories")
  category = db.relationship("Categories", back_populates="products")

  def __init__(self, product_id, category_id):
    self.product_id = product_id
    self.category_id = category_id


class ProductsCategoriesXrefSchema(ma.Schema):
  class Meta:
    fields = ['product_id', 'category_id', 'category']

  product_id = ma.fields.UUID()
  category_id = ma.fields.UUID()
  
  category = ma.fields.Nested("CategorySchema", only=['category_id', 'category_name'])


xref_schema = ProductsCategoriesXrefSchema()
xrefs_schema = ProductsCategoriesXrefSchema(many=True)