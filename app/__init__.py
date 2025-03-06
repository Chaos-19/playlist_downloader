from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend="redis://localhost:6379/0",
        broker="redis://localhost:6379/0"
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
    
app.register_blueprint(main)
app.register_blueprint(api_ytvd,url_prefix="/api")

'''
from flask import Flask

from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery



def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    from app.routes import main
    from app.blueprints.yt_downloader import api_ytvd
    
    app.register_blueprint(main)
    app.register_blueprint(api_ytvd,url_prefix="/api")
    
    celery = make_celery(app)

    return app
'''