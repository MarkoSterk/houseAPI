from flask import abort, jsonify
from werkzeug.exceptions import HTTPException

##function for raising exception when needed.
def AppError(msg, statusCode):
    response = jsonify({
        'status': 'error',
        'message': msg,
        'code': statusCode
        })
    response.status_code = statusCode
    return abort(response)


###function for exception handling
def handle_error(err):
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    
    if code == 500:
        err.description('An error occured. Please come back later. We are sorry.')
    
    return jsonify({
        'status': 'error',
        'message': err.description,
        'code': code
    }), code   