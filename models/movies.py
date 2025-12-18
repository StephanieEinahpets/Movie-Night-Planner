import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.movie_votes_xref import movie_votes_association_table


class Movies(db.Model):
  __tablename__ = 'Movies'

  movie_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  recommender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=True)
  title = db.Column(db.String(), nullable=False, unique=True)
  genre = db.Column(db.String())
  synopsis = db.Column(db.String())

  recommender = db.relationship("AppUsers", back_populates="recommended_movies")
  movie_image = db.relationship("MovieImages", back_populates="movie", uselist=False, cascade="all, delete-orphan")
  movie_votes = db.relationship("MovieVotes", secondary=movie_votes_association_table,back_populates="movies")
  movie_nights = db.relationship("MovieNights", back_populates="selected_movie")

  def __init__(self, title, recommender_id=None, genre=None, synopsis=None):
    self.title = title
    self.recommender_id = recommender_id
    self.genre = genre
    self.synopsis = synopsis

  def new_movie_obj():
    return Movies('', None, '', '')


class MoviesSchema(ma.Schema):
  class Meta:
    fields = ['movie_id', 'title', 'genre', 'synopsis', 'recommender_id', 'recommender', 'movie_image']

  movie_id = ma.fields.UUID()
  title = ma.fields.String(required=True)
  genre = ma.fields.String()
  synopsis = ma.fields.String()
  recommender_id = ma.fields.UUID()
  recommender = ma.fields.Nested("AppUsersSchema", only=['user_id', 'username', 'email'])
  movie_image = ma.fields.Nested("MovieImagesSchema", exclude=['movie'])


movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)