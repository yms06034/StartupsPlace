from flask import Flask
from flask import render_template, g
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    print('run: create_app()')
    app = Flask(__name__)

    """Flask Configs"""
    from .configs import DevelopmentConfig, ProducttionConfig

    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProducttionConfig()

    print('run config', config)
    app.config.from_object(config)

    """ CSRF INIT """
    csrf.init_app(app)

    """ DB INIT """
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    """ ROUTES INIT """
    from startupsplace.routes import base_route
    from startupsplace.routes import auth_route
    from startupsplace.routes import chart_route

    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.auth_bp)
    app.register_blueprint(chart_route.chart_bp)

    """ RESTX INIT """
    from startupsplace.apis import blueprint as api

    app.register_blueprint(api)

    """ REQUEST HOOK """
    @app.before_request
    def before_requset():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html')

    return app

