from flask import Flask, jsonify, make_response
from flask_principal import Principal
from flask_migrate import Migrate
from flask_cors import CORS
from flask_principal import identity_loaded

from app import db, ma
from app.lib.wsgi.ReverseProxied import ReverseProxied
from app.api_admin.authentication import auth, Authentication

def create_app(config):

    # init app
    app = Flask(__name__)
    app.config.from_object(config)

    # init authorization
    Principal(app)

    # init CORS
    if 'CORS_ORIGIN' in app.config:
        CORS(app, supports_credentials=True, origin=app.config['CORS_ORIGIN'])

    # init database
    db.init_app(app)
    Migrate(app, db)

    # init Marshmallow
    ma.init_app(app)

    # add support for URI versioning via web server
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    # AUTHENTICATION

    @auth.verify_password
    def verify_password(username_or_token, password):
        return Authentication.verify_password(username_or_token, password)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        return Authentication.on_identity_loaded(sender, identity)

    # ERRORS

    @app.errorhandler(400)
    def error_400(error):
        return make_response(jsonify({'error': 'Bad data'}), 400)

    @app.errorhandler(401)
    def error_401(error):
        return make_response(jsonify({'error': error.description}), 401)

    @app.errorhandler(403)
    def error_403(error):
        return make_response(jsonify({'error': error.description if error.description else "Permission denied"}), 403)

    @app.errorhandler(404)
    def error_404(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(405)
    def error_405(error):
        return make_response(jsonify({'error': 'Method not allowed'}), 405)

    @app.errorhandler(500)
    def error_500(error):
        return make_response(jsonify({'error': 'Server error'}), 500)

    # ROUTES

    from app.api_admin.routes.app_keys import app_keys as app_keys_blueprint
    app.register_blueprint(app_keys_blueprint)

    from app.api_admin.routes.auth_token import auth_token as auth_token_blueprint
    app.register_blueprint(auth_token_blueprint)

    from app.api_admin.routes.password import password as password_blueprint
    app.register_blueprint(password_blueprint)

    from app.api_admin.routes.user_account import user_account as user_account_blueprint
    app.register_blueprint(user_account_blueprint)

    from app.api_admin.routes.roles import roles as roles_blueprint
    app.register_blueprint(roles_blueprint)

    from app.api_admin.routes.administrators import administrators as administrators_blueprint
    app.register_blueprint(administrators_blueprint)

    from app.api_admin.routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from app.api_admin.routes.user_profiles import user_profiles as user_profiles_blueprint
    app.register_blueprint(user_profiles_blueprint)

    from app.api_admin.routes.password_resets import password_resets as password_resets_blueprint
    app.register_blueprint(password_resets_blueprint)

    from app.api_admin.routes.terms_of_service import terms_of_service as terms_of_service_blueprint
    app.register_blueprint(terms_of_service_blueprint)

    from app.api_admin.routes.logins import logins as logins_blueprint
    app.register_blueprint(logins_blueprint)

    from app.api_admin.routes.notifications import notifications as notifications_blueprint
    app.register_blueprint(notifications_blueprint)

    from app.api_admin.routes.countries import countries as countries_blueprint
    app.register_blueprint(countries_blueprint)

    from app.api_admin.routes.regions import regions as regions_blueprint
    app.register_blueprint(regions_blueprint)

    return app
