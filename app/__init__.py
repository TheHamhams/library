from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)