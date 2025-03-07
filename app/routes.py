import logging
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.before_request
def log_request():
    logging.info(f"Incoming request: {request.method} {request.url} | Body: {request.data.decode('utf-8') if request.data else 'No Body'}")

@main.route('/')
def home():
    return 'The project page'

@main.route('/about') 
def about():
    return 'The about page'