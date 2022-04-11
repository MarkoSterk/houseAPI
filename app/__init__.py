from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

from werkzeug.exceptions import default_exceptions

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_mail_sendgrid import MailSendGrid

from flask_jwt_extended import JWTManager

from .controllers import errorController
from app.config import Config

"""
Main entry point of the app. 
It needs a Config object which is located in the same folder (config.py)
"""

mongo = PyMongo() ##creates mongoDB instance
bcrypt = Bcrypt() ##creates Bcrypt instance
jwt = JWTManager() ##creates JSON Web Token Manager instance
mail = MailSendGrid() ##creates sendgrid instance

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    
    ##registers/initializes all extensions 
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    #limiter - prevents flooding of the app with requests
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    ##registers userRoutes blueprint
    from app.routes.users.userRoutes import userRoutes
    app.register_blueprint(userRoutes)

    ##registers houseRoutes blueprint
    from app.routes.houses.houseRoutes import houseRoutes
    app.register_blueprint(houseRoutes)

    ##sets the maximum hourly request rate from one IP
    ##to the userRoutes and houseRoutes
    limiter.limit("200/hour")(userRoutes)
    limiter.limit("200/hour")(houseRoutes)
    
    ##override the default exception responses and replace them with handle_error
    for ex in default_exceptions:
        app.register_error_handler(ex, errorController.handle_error)

    return app
    
    
