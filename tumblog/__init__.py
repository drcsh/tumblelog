import os

from flask import Flask
from mongoengine import connect
from .views.home import home
from .views.user import user

# Initialize main App
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@" \
                          f"{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}"
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Initialize modules (Blueprints)
app.register_blueprint(home)
app.register_blueprint(user)

# Connect to Mongo Engine
connect(host=app.config["MONGO_URI"])


import tumblog.views