from flask import Flask
from celery import Celery
import os
import logging

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ.get('REDIS_URL'),
        broker=os.environ.get('REDIS_URL')
    )
    celery.conf.update(app.config)
    return celery

# Initialize Flask
app = Flask(__name__)
app.config.from_object('config')

# Initialize Celery
celery = make_celery(app)

# Import blueprints after initializing app
from app.routes import main
from app.blueprints.yt_downloader import api_ytvd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@main.before_request
def log_request():
    logging.info(f"Incoming request: {request.method} {request.url} | Body: {request.data.decode('utf-8') if request.data else 'No Body'}")

    
app.register_blueprint(main)
app.register_blueprint(api_ytvd,url_prefix="/api")
