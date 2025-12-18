import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class AppUsers(db.Model):
  __tablename__ = 'AppUsers'

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = db.Column(db.String(), nullable=False, unique=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  role = db.Column(db.String(), default='user')

  auth = db.relationship("AuthTokens", back_populates="user", cascade="all, delete-orphan")
  recommended_movies = db.relationship("Movies", back_populates="recommender")
  hosted_movie_nights = db.relationship("MovieNights", back_populates="host")
  movie_votes = db.relationship("MovieVotes", back_populates="user", cascade="all, delete-orphan")
  snacks = db.relationship("Snacks", back_populates="user", cascade="all, delete-orphan")

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

  def new_user_obj():
    return AppUsers('', '', '')


class AppUsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id', 'username', 'email', 'role']

  user_id = ma.fields.UUID()
  username = ma.fields.String(required=True)
  email = ma.fields.String(required=True)
  role = ma.fields.String()


app_user_schema = AppUsersSchema()
app_users_schema = AppUsersSchema(many=True)