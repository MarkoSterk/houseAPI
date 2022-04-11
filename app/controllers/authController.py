from flask import jsonify, request
from ..routes.users import userRoutes
import datetime
from functools import wraps
from flask_jwt_extended import current_user
from flask_jwt_extended import unset_jwt_cookies, unset_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity

from ..models.userModel import User
from .errorController import AppError
from app import jwt, bcrypt

def login():
    #user = User.findOne({'_id': request.get_json()['_id']}, showHiddenFields=True)
    if (('email' or 'password') not in request.get_json().keys()):
        return AppError('Missing input fields!', 400)

    user = User.findOne({'email': request.get_json()['email']}, hideFields=[])

    if not user:
        return AppError('User with this email does not exist', 404)

    if bcrypt.check_password_hash(user['password'], request.get_json()['password'])==False:
        return AppError('Wrong password', 400)
    
    msg = f'User {user["name"]} logged in successfully.'
    access_token = create_access_token(identity=user['_id'])

    response = jsonify({
            'status': 'success',
            'data': None,
            'message': msg,
            'access_token': access_token
        })
    set_access_cookies(response, access_token)
    return response, 200

def logout():
    print(current_user)
    if not current_user:
        return AppError('You are not logged in', 400)
    
    response = jsonify({
        'status': 'success',
        'data': None,
        'message': 'logout successful'
        })
    unset_jwt_cookies(response)
    unset_access_cookies(response)
    return response


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 'error',
        'message': 'Your access token has expired. Please login again',
        'code': 401
    }), 401

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    iat = jwt_data['iat']
    user = User.findOne({'_id': identity}, hideFields=[])
    if not user: return AppError('User with the provided identity does not exist', 404)
    passwordChangedAt = 0
    if 'passwordChangedAt' in user.keys():
        passwordChangedAt = int(datetime.datetime.strptime(user['passwordChangedAt'], "%Y-%m-%d %H:%M:%S").strftime("%s"))
    
    if iat<passwordChangedAt: return AppError('You recently changed your password. Please sign in again', 401)

    del user['password']
    del user['_v']
    del user['_createdAt']
    return user


def refreshExpiringJWTS(response):
    try:
        print('Here')
        exp_timestamp = get_jwt()["exp"]
        now = datetime.datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=60))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


def role_required(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user['role'] not in access_level:
                return AppError(f'You do not have the required access level', 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator