import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Warranties(db.Model):
  __tablename__ = 'Warranties'

  warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Products.product_id'), nullable=False)
  warranty_months = db.Column(db.String(), nullable=False)

  product = db.relationship("Products", back_populates="warranty")

  def __init__(self, product_id, warranty_months):
    self.product_id = product_id
    self.warranty_months = warranty_months

  def new_warranty_obj():
    return Warranties('', '')


class WarrantySchema(ma.Schema):
  class Meta:
    fields = ['warranty_id', 'product_id', 'warranty_months']

  warranty_id = ma.fields.UUID()
  product_id = ma.fields.UUID(required=True)
  warranty_months = ma.fields.String(required=True)


warranty_schema = WarrantySchema()
warranties_schema = WarrantySchema(many=True)