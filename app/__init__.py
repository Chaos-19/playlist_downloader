from flask import Flask
from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ.get('REDIS_URL'),
        broker=os.environ.get('REDIS_URL')
    )
    celery.conf.update(app.config)h
    return celery

# Initialize Flask
app = Flask(__name__)
app.config.from_object('config')

# Initialize Celery
celery = make_celery(app)

# Import blueprints after initializing app
from app.routes import main
from app.blueprints.yt_downloader import api_ytvd
    
app.register_blueprint(main)
app.register_blueprint(api_ytvd,url_prefix="/api")