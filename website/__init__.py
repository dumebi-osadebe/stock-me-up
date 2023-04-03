from flask import Flask
from flask_restful import Resource, Api

def create_app():
    app = Flask(__name__)
    #api = Api(app)
    app.config['SECRET_KEY'] = '123_dumebi'

    from .app import a 
    app.register_blueprint(a, url_prefix='/')

    from .views import views # importing the variable views in file views.py
    app.register_blueprint(views, url_prefix='/')



    return app
