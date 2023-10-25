from flask import Flask
from .views import views,static_bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(static_bp, url_prefix='/static')
    # app.config['UPLOAD_FOLDER'] = 'D:/VisualContentPlatform/website/uploads'  # Set your upload folder path
    # app.config['UPLOAD_URL_PATH'] = '/uploads'
    # app.register_blueprint(uploads,url_prefix='/uploads')
    # app.register_blueprint(temp)
    return app