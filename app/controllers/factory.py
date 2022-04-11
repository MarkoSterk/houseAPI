from flask import jsonify, request, current_app
from .errorController import AppError

def getAll(model, hideFields=[]):
    query = model.find({}, hideFields=hideFields)
    return jsonify({
        'status': 'success',
        'data': query,
        'message': 'Query completed successfully'
    }), 200


def getOne(id, model, populate=False, populateFields=[], hideFields=[]):
    query = model.findOne({'_id': id}, hideFields=hideFields)
    if populate:
        query = model.populateField(query, populateFields[0], populateFields[1])
    return jsonify({
        'status': 'success',
        'data': query,
        'message': 'Query completed successfully'
    }), 200


def deleteOne(id, model):
    query = model.findOne({'_id': id})
    if not query:
        return AppError(f'{model.__name__} with this id does not exist', 404)
    
    try:
        model.deleteOne({'_id': id})
    except:
        return AppError('There was a problem. Please try again a bit later', 500)
    
    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'{model.__name__} deleted successfully'
    }), 204

