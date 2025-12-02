import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class AppUsers(db.Model):
  __tablename__ = 'AppUsers'

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Companies.company_id'), nullable=False)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  phone = db.Column(db.String())
  active = db.Column(db.Boolean(), default=True)
  role = db.Column(db.String(), nullable=False, default='user')

  company = db.relationship("Companies", back_populates="users")
  auth = db.relationship("AuthTokens", back_populates="user", cascade="all, delete-orphan")

  def __init__(self, company_id, first_name, last_name, email, password, phone=None, active=True, role='user'):
    self.company_id = company_id
    self.first_name = first_name
    self.last_name = last_name 
    self.email = email
    self.password = password
    self.phone = phone
    self.active = active 
    self.role = role

  def new_user_obj():
    return AppUsers('', '', '', '', '', None, True, 'user')
  

class AppUsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id', 'company_id', 'first_name', 'last_name', 'email', 'phone', 'active', 'role', 'company']

  user_id = ma.fields.UUID()
  company_id = ma.fields.UUID(required=True)
  first_name = ma.fields.String(required=True)
  last_name = ma.fields.String(required=True)
  email = ma.fields.String(required=True)
  phone = ma.fields.String(allow_none=True)
  active = ma.fields.Boolean(required=True, dump_default=True)
  role = ma.fields.String(required=True, dump_default='user')

  company = ma.fields.Nested("CompanySchema", exclude=['users'])


app_user_schema = AppUsersSchema()
app_users_schema = AppUsersSchema(many=True)
