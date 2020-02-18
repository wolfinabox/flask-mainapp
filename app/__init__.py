from flask import Flask
from flask_cors import CORS,cross_origin
from app.config import Config
app = Flask(__name__,static_url_path='')
cors=CORS(app)
app.config.from_object(Config())
from app import routes
from app import errors