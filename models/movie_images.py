import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class MovieImages(db.Model):
  __tablename__ = 'MovieImages'

  movie_image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Movies.movie_id'), nullable=False, unique=True)
  movie_image_url = db.Column(db.String(), nullable=False)

  movie = db.relationship("Movies", back_populates="movie_image")

  def __init__(self, movie_id, movie_image_url):
    self.movie_id = movie_id
    self.movie_image_url = movie_image_url

  def new_movie_image_obj():
    return MovieImages(None, '')


class MovieImagesSchema(ma.Schema):
  class Meta:
    fields = ['movie_image_id', 'movie_id', 'movie_image_url', 'movie']

  movie_image_id = ma.fields.UUID()
  movie_id = ma.fields.UUID(required=True)
  movie_image_url = ma.fields.String(required=True)
  movie = ma.fields.Nested("MoviesSchema", only=['movie_id', 'title'])


movie_image_schema = MovieImagesSchema()
movie_images_schema = MovieImagesSchema(many=True)