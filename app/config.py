import os
from datetime import timedelta

###It is recommended that you save sensitive configuration data as environment variables
##access them using the os module: os.environ.get('NAME_OF_VARIABLE')

class Config:
    SECRET_KEY='primary-super-secret-app-key' ##JWT_SECRET_KEY and SECRET_KEY can be the same.

    JWT_SECRET_KEY='your-super-secret-string'
    JWT_TOKEN_LOCATION=["cookies"]
    JWT_COOKIE_SECURE=False
    JWT_CSRF_IN_COOKIES=True
    JWT_COOKIE_CSRF_PROTECT =False ###Should be set to True when in production
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=90) ##expiration duration of access tokens

    PASS_RESET_TOKEN_DURATION = '600000' ##expiration duration of password reset token

    MAIL_SENDGRID_API_KEY='sendgrid_API_key'
    MAIL_SENDGRID_SENDER='marko_sterk@hotmail.com' ##validated email for sendgrid sender

    MONGO_URI="mongodb+srv://marko:m314159265S@cluster0.xpomk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"