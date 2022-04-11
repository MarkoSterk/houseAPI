from flask import jsonify, request, url_for, current_app
from flask_jwt_extended import current_user, set_access_cookies, create_access_token
from app import bcrypt
import os
import datetime

from .errorController import AppError
from ..models.userModel import User
from ..utils.email import sendPasswordResetToken
from ..utils.helperFuncs import hashUrlSafe
from .factory import deleteOne, getAll, getOne


def getAllUsers():
    return getAll(User, hideFields=['password', 'passwordChangedAt', '_v', 'active'])

def getUser(userId):
    return getOne(userId, User, hideFields=['password', 'passwordChangedAt', '_v', 'active'])

def deleteUser(userId):
    return deleteOne(userId, User)


def updateUser():
    if(('password' in request.get_json().keys()) or ('passwordConfirm' in request.get_json().keys())):
        return AppError('This route is not for password updates. Please use /updatePassword', 400)
    
    filteredData = User.filterRequestBody(request.get_json())
    if(('role' in filteredData.keys()) and (current_user['role']!='admin')): del filteredData['role']

    user = User.findOne({'_id': current_user['_id']})
    if not user:
        return AppError('User with this id does not exist', 404)

    user = User.updateOne({'_id': current_user['_id']},
                            { "$set": filteredData },
                            validate=True, returnNew=True,
                            hideFields=['password', 'passwordChangedAt', '_v', 'active'])

    return jsonify({
        'status': 'success',
        'data': user,
        'message': f'User updated successfully'
    }), 200


def signup():
    #print(request.get_json())
    user = User(request.get_json())
    user.save()
    user = vars(user)
    del user['password']
    response = jsonify({
        'status': 'success',
        'data': user,
        'message': 'Sign up successfull.'
    })
    access_token = create_access_token(identity=user['_id'])
    set_access_cookies(response, access_token)
    return response, 200


def updatePassword():
    if ('currentPassword' or 'newPassword' or 'confirmNewPassword') not in request.get_json().keys():
        return AppError('Input field missing', 400)

    currentPassword = request.get_json()['currentPassword']
    newPassword = request.get_json()['newPassword']
    confirmNewPassword = request.get_json()['confirmNewPassword']

    user = User.findOne({'_id': current_user['_id']}, hideFields=[])

    if(newPassword!=confirmNewPassword):
        return AppError('New/confirm passwords dont match.', 400)
    if bcrypt.check_password_hash(user['password'], currentPassword)==False:
        return AppError('Wrong (current) password.', 400)

    pwHash = bcrypt.generate_password_hash(newPassword).decode('utf-8')
    passwordChangedAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = User.updateOne({'_id': current_user['_id']},
                    {'$set': {'password': pwHash, 'passwordChangedAt': passwordChangedAt}},
                    returnNew=True)

    del user['password']

    response = jsonify({
        'status': 'success',
        'data': user,
        'message': 'Password was updated successfully.'
    })
    access_token = create_access_token(identity=current_user['_id'])
    set_access_cookies(response, access_token)
    return response, 200


def resetPasswordToken():
    user = User.findOne({'email': request.get_json()['email']}, hideFields=['password', 'passwordChangedAt', '_v'])
    if not user: return AppError('User with this email does not exist', 404)

    exp_time = int(datetime.datetime.utcnow().timestamp()) + int(current_app.config['PASS_RESET_TOKEN_DURATION'])
    
    reset_token = hashUrlSafe(current_app.config['SECRET_KEY'])

    user = User.updateOne({'_id': user['_id']},
                        {'$set': {'password_reset_token': reset_token,
                                    'password_reset_expires': exp_time}},
                        validate=False, returnNew=True)


    ####Change the URL string to a valid string once in production (add base url + protocol)
    sendPasswordResetToken(request.get_json()['email'], f"{url_for('userRoutes.resetPassword', reset_token=reset_token)}")

    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'Password reset token sent to {user["email"]}'
    }), 200


def resetPassword(reset_token):

    user = User.findOne({'password_reset_token': reset_token})
    if not user:
        return AppError('Invalid reset token. User does not exist.', 404)

    if int(user['password_reset_expires']) < int(datetime.datetime.utcnow().timestamp()):
        return AppError('This password reset token expired. Please get a new one!'), 400

    if bcrypt.check_password_hash(reset_token, current_app.config['SECRET_KEY'])==False:
        return AppError('Corrupt password reset URL.', 401)
    
    password, passwordConfirm = request.get_json()['password'], request.get_json()['passwordConfirm']
    if password != passwordConfirm:
        return AppError('Passwords must match!', 400)

    newPassHash = bcrypt.generate_password_hash(password).decode('utf-8')

    User.updateOne({'_id': user['_id']},
                    {'$set': {'password': newPassHash},
                    '$unset': {'password_reset_token': '',
                                'password_reset_expires': ''}},
                    validate=False)

    return jsonify({
        'status': 'success',
        'message': 'Password was reset successfully'
    }), 200


