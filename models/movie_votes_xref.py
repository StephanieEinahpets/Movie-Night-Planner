from db import db

movie_votes_association_table = db.Table(
  "MovieVotesAssociation",
  db.Model.metadata,
  db.Column("movie_id", db.ForeignKey("Movies.movie_id", ondelete="CASCADE"), primary_key=True),
  db.Column("movie_vote_id", db.ForeignKey("MovieVotes.movie_vote_id", ondelete="CASCADE"), primary_key=True)
)
