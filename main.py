import logging
import os
from logging.config import fileConfig

import flask_restless
from flask import Flask, send_file
from flask_login import login_required

import app.constants as constants
from app.auth.fido2_mgmt import auth_blueprint
from app.auth.login_mgmt import login_blueprint, login_manager
from app.auth.restless_preprocessors import auth_preprocessors, user_api_preprocessors
from app.database import db, ma
from app.model.user import User
from app.model.user_credential import UserCredential
from app.apis import api as restx_api


fileConfig(constants.LOGGING_CONF)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path="", static_folder=constants.STATIC_FILES_DIR)
app.secret_key = os.urandom(32)  # Used for session.
app.config['SQLALCHEMY_DATABASE_URI'] = constants.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(auth_blueprint)
app.register_blueprint(login_blueprint)

db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)
# Flask RestX
restx_api.init_app(app)

db.create_all(app=app)

# Flask Restless
# Use the preprocessor to validate if the user is authenticated before processing any request.
api_manager = flask_restless.APIManager(app, session=db.session, preprocessors=auth_preprocessors)

with app.app_context():
    # Use the preprocessor to validate the user can only get/update his/her data.
    api_manager.create_api(User, methods=['GET', 'PATCH'], preprocessors=user_api_preprocessors)
    api_manager.create_api(UserCredential, methods=['GET', 'PATCH'], preprocessors=user_api_preprocessors)
# END Flask Restless


@app.route('/')
@login_required
def index():
    return send_file(f'{constants.UI_RESOURCE_ROOT}/index.html')


def main():
    # FIDO2 needs SSL
    app.run(ssl_context="adhoc")


if __name__ == '__main__':
    main()
