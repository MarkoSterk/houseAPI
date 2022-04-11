from flask import request, Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from ...controllers import userController, authController

userRoutes=Blueprint('userRoutes',__name__)


@userRoutes.route("/api/v1/users", methods=['GET'])
@jwt_required()
def users():  
    return userController.getAllUsers()


@userRoutes.route("/api/v1/users/<string:userId>", methods=['GET'])
@jwt_required()
def user(userId):  
    return userController.getUser(userId)


@userRoutes.route("/api/v1/users/signup", methods=['POST'])
def signup():  
    return userController.signup()


@userRoutes.route("/api/v1/users/login", methods=['POST'])
def login():  
    return authController.login()


@userRoutes.route("/api/v1/users/logout", methods=['GET'])
@jwt_required()
def logout():  
    return authController.logout()


@userRoutes.route("/api/v1/users/update", methods=['PATCH'])
@jwt_required()
def update():  
    return userController.updateUser()


@userRoutes.route("/api/v1/users/updatePassword", methods=['PATCH'])
@jwt_required()
def updatePass():  
    return userController.updatePassword()


@userRoutes.route("/api/v1/users/resetPasswordToken", methods=['POST'])
def resetPasswordToken():
    return userController.resetPasswordToken()


@userRoutes.route("/api/v1/users/resetPassword/<string:reset_token>", methods=['POST'])
def resetPassword(reset_token):
    return userController.resetPassword(reset_token)


@userRoutes.route("/api/v1/users/<string:userId>", methods=['DELETE'])
@jwt_required()
def delete(userId):  
    return userController.deleteUser(userId)


@userRoutes.after_request
def refresh_expiring_jwts(response):
    return authController.refreshExpiringJWTS(response)