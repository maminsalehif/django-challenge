from flask import Flask
from flask_cors import CORS

from webapi.views import api_bp


def create_app(name):
    app = Flask(name, static_url_path='/uploaded_files', static_folder='uploaded_files')
    CORS(app)

    app.register_blueprint(api_bp)

    return app
