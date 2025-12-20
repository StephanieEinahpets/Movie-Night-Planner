import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.movie_votes_xref import movie_votes_association_table

class MovieVotes(db.Model):
  __tablename__ = 'MovieVotes'

  movie_vote_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=False)
  voted_for = db.Column(db.Boolean, nullable=False)

  user = db.relationship("AppUsers", back_populates="movie_votes")
  movies = db.relationship("Movies", secondary=movie_votes_association_table, back_populates="movie_votes")

  def __init__(self, user_id, voted_for=None):
    self.user_id = user_id
    self.voted_for = voted_for

  # def new_movie_vote_obj():
  #   return MovieVotes('', None)


class MovieVotesSchema(ma.Schema):
  class Meta:
    fields = ['movie_vote_id', 'user_id', 'voted_for', 'user', 'movies']

  movie_vote_id = ma.fields.UUID()
  user_id = ma.fields.UUID(required=True)
  voted_for = ma.fields.Boolean()
  user = ma.fields.Nested("AppUsersSchema", only=['user_id', 'username', 'email'])
  movies = ma.fields.Nested("MoviesSchema", many=True, only=['movie_id', 'title'])

movie_vote_schema = MovieVotesSchema()
movie_votes_schema = MovieVotesSchema(many=True)