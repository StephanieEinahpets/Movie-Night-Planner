import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.movie_votes_xref import movie_votes_association_table


class MovieNights(db.Model):
  __tablename__ = 'MovieNights'

  movie_night_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  host_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=False)
  selected_movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Movies.movie_id'), nullable=True)
  date = db.Column(db.DateTime(), nullable=False)
  location = db.Column(db.String())

  host = db.relationship("AppUsers", back_populates="hosted_movie_nights")
  selected_movie = db.relationship("Movies", back_populates="movie_nights")
  snacks = db.relationship("Snacks", back_populates="movie_night", cascade="all, delete-orphan")

  def __init__(self, host_user_id, date, selected_movie_id=None, location=None):
    self.host_user_id = host_user_id
    self.selected_movie_id = selected_movie_id
    self.date = date
    self.location = location

  def new_movie_night_obj():
    return MovieNights(None, None, None, '')


class MovieNightsSchema(ma.Schema):
  class Meta:
    fields = ['movie_night_id', 'host_user_id', 'selected_movie_id', 'date', 'location', 'host', 'selected_movie', 'snacks']

  movie_night_id = ma.fields.UUID()
  host_user_id = ma.fields.UUID(required=True)
  selected_movie_id = ma.fields.UUID()
  date = ma.fields.DateTime(required=True)
  location = ma.fields.String()
  host = ma.fields.Nested("AppUsersSchema", only=['user_id', 'username', 'email'])
  selected_movie = ma.fields.Nested("MoviesSchema", only=['movie_id', 'title', 'genre'])
  snacks = ma.fields.Nested("SnacksSchema", many=True, exclude=['movie_night'])


movie_night_schema = MovieNightsSchema()
movie_nights_schema = MovieNightsSchema(many=True)