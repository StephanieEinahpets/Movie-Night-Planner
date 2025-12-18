import routes

def register_blueprint(app):
  app.register_blueprint(routes.auth)
  app.register_blueprint(routes.search)
  app.register_blueprint(routes.users)
  app.register_blueprint(routes.movies)
  app.register_blueprint(routes.movienights)
  app.register_blueprint(routes.movievotes)
  app.register_blueprint(routes.movieimages)
  app.register_blueprint(routes.snacks)