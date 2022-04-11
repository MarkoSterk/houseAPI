from flask import jsonify, request, current_app
from flask_jwt_extended import current_user

from .errorController import AppError
from ..models.houseModel import House
from ..models.userModel import User
from .factory import getAll, getOne, deleteOne
from ..utils.helperFuncs import parseFormData, saveImageFiles

"""
Controllers for all house routes.
"""

def getAllHouses():
    return getAll(House)

def getHouse(houseId):
    return getOne(houseId, House, populate=True, populateFields=['seller', User], hideFields=[])

def deleteHouse(houseId):
    return deleteOne(houseId, House)

def createHouse():

    data = parseFormData(request.form, skip=['images'])
    data = House.filterRequestBody(data, skip=['images'])
    data['seller']=current_user['_id']
    if request.files:
        data['images']=saveImageFiles(request.files.getlist('images'))

    house = House(data)
    house.save()

    return jsonify({
        'status': 'success',
        'data': vars(house),
        'message': 'House created successfully'
    }), 200


def updateHouse(houseId):
    house = House.findOne({'_id': houseId})
    if not house:
        return AppError('House with this id does not exist.', 404)
    
    if house['seller']!=current_user['_id']:
        return AppError('This is not your house', 401)
    
    data = parseFormData(request.form, skip=['images'])
    data = House.filterRequestBody(data, skip=['images'])
    if 'seller' in data.keys(): del data['seller']

    if request.files:
        data['images']=saveImageFiles(request.files.getlist('images'))

    house = House.updateOne({'_id': houseId}, {'$set': data}, validate=True, returnNew=True)

    return jsonify({
        'status': 'success',
        'data': house,
        'message': 'House updated successfully'
    }), 200


