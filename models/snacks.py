import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Snacks(db.Model):
  __tablename__ = 'Snacks'

  snack_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  movie_night_id = db.Column(UUID(as_uuid=True), db.ForeignKey('MovieNights.movie_night_id'), nullable=False)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=False)
  snack_name = db.Column(db.String(), nullable=False)

  movie_night = db.relationship("MovieNights", back_populates="snacks")
  user = db.relationship("AppUsers", back_populates="snacks")

  def __init__(self, movie_night_id, user_id, snack_name):
    self.movie_night_id = movie_night_id
    self.user_id = user_id
    self.snack_name = snack_name

  def new_snack_obj():
    return Snacks(None, None, '')


class SnacksSchema(ma.Schema):
  class Meta:
    fields = ['snack_id', 'movie_night_id', 'user_id', 'snack_name', 'movie_night', 'user']

  snack_id = ma.fields.UUID()
  movie_night_id = ma.fields.UUID(required=True)
  user_id = ma.fields.UUID(required=True)
  snack_name = ma.fields.String(required=True)
  movie_night = ma.fields.Nested("MovieNightsSchema", only=['movie_night_id', 'date', 'location'])
  user = ma.fields.Nested("AppUsersSchema", only=['user_id', 'username'])


snack_schema = SnacksSchema()
snacks_schema = SnacksSchema(many=True)