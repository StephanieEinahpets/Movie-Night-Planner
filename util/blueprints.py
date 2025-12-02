import routes

def register_blueprint(app):
  app.register_blueprint(routes.auth)
  app.register_blueprint(routes.search)
  app.register_blueprint(routes.users)
  app.register_blueprint(routes.companies)
  app.register_blueprint(routes.categories)
  app.register_blueprint(routes.products)
  app.register_blueprint(routes.warranties)