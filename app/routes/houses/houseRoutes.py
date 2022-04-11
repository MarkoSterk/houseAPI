from flask import request, Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from ...controllers import houseController
from ...controllers.authController import role_required


"""
All house routes combined into a blueprint
"""

houseRoutes = Blueprint('houseRoutes',__name__)

@houseRoutes.route("/api/v1/houses", methods=['GET'])
def houses():  
    return houseController.getAllHouses()


@houseRoutes.route("/api/v1/houses/<string:houseId>", methods=['GET'])
def getHouse(houseId):  
    return houseController.getHouse(houseId)


@houseRoutes.route("/api/v1/houses", methods=['POST'])
@jwt_required()
@role_required(['admin'])
def createHouse():  
    return houseController.createHouse()


@houseRoutes.route("/api/v1/houses/<string:houseId>", methods=['PATCH'])
@jwt_required()
def updateHouse(houseId):  
    return houseController.updateHouse(houseId)


@houseRoutes.route("/api/v1/houses/<string:houseId>", methods=['DELETE'])
@jwt_required()
def deleteHouse(houseId):  
    return houseController.deleteHouse(houseId)
