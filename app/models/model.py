import collections
from distutils.log import error
from typing import Collection
from app import mongo
from flask import abort, jsonify
import secrets
import datetime
from validate_email import validate_email
from xmlrpc.client import Boolean, boolean

class Model:
    collection: str = 'db'
    Schema = {}
    hideFields = []

    def __init__(self, modelData):
        self._id = secrets.token_hex(16)
        self._v = 0
        self._createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        ##checks if required fields are present in modelData
        ##checks if unique fields setisfy the requirement
        Model.validateInit(self.Schema, modelData, self.collection)

        for key in modelData.keys():
            if key in self.Schema:
                setattr(self, key, modelData[key])

    def __repr__(self):
        return f'{self.collection}(_id: {self._id}, _v: {self._v}, _createdAt: {self._createdAt})'

    ####Input validation
    def isEmail(fieldname, data, check, schema=False):
        is_valid = bool(validate_email(data[fieldname]))
        if is_valid != check:
            Model.error('Validation error', 'This is not a valid email address', 400)
    
    def checkElementsType(fieldname, modelData, checkType, schema=False):
        if type(checkType) is tuple:
            errorStr = [checkEl.__name__ for checkEl in checkType]
            setType=checkType[-1]
        else:
            errorStr = checkType.__name__
            setType=checkType
        if hasattr(modelData[fieldname], '__getitem__'):
            for i, el in enumerate(modelData[fieldname]):
                if isinstance(el, checkType) == False:
                    try:
                        modelData[fieldname][i]=setType(modelData[fieldname][i])
                    except:
                        Model.error('Validation error', f'{fieldname} can contain only {errorStr} data', 400)


    def minValue(fieldname, data, N, schema=False):
        if data[fieldname]<N:
            Model.error('Validation error', f'{fieldname} can not be smaller than {N}.', 400)
    
    def maxValue(fieldname, data, N, schema=False):
        if data[fieldname]>N:
            Model.error('Validation error', f'{fieldname} can not be larger than {N}.', 400)

    def isLength(fieldname, data, N, schema=False):
        if len(data[fieldname])!=N:
            Model.error('Validation error', f'{fieldname} must have size {N}', 400)

    def minLength(fieldname, data, N, schema=False):
        if len(data[fieldname])<N:
            Model.error('Validation error', f'{fieldname} must be at least {N} characters long.', 400)
    
    def maxLength(fieldname, data, N, schema=False):
        if len(data[fieldname])>N:
            Model.error('Validation error', f'{fieldname} can not be longer than {N} characters.', 400)
    
    def mustMatch(fieldname, data, matchField, schema=False):
        if data[fieldname]!=data[matchField]:
            Model.error('Validation error', f'{fieldname} and {matchField} must match!', 400)

    def insertDefaults(Schema, modelData):
        for key in Schema.keys():
            if(('default' in Schema[key].keys())
                and (key not in modelData.keys())):
                modelData[key] = Schema[key]['default']

    def checkTypes(Schema, modelData):
        for key in Schema.keys():
            if key in modelData.keys():
                if type(Schema[key]['type']) is tuple:
                    errorStr = [checkEl.__name__ for checkEl in Schema[key]['type']]
                    setType = Schema[key]['type'][-1]
                else:
                    errorStr = Schema[key]['type'].__name__
                    setType = Schema[key]['type']

                if isinstance(modelData[key], Schema[key]['type']) == False:
                    try:
                        modelData[key] = setType(modelData[key])
                    except:
                        Model.error('Validation error', f'{key} must be of type {errorStr}', 400)
        return modelData
    
    def checkRequired(Schema, modelData):
        for key in Schema.keys():
            if 'required' in Schema[key].keys():
                if Schema[key]['required']==True:
                    if key not in modelData.keys():
                        Model.error('Validation error', f'{key} is a required field', 400)

    def checkUnique(Schema, modelData, collection, schema=False):
        for key in Schema.keys():
            if 'unique' in Schema[key].keys():
                if Schema[key]['unique']:
                    if mongo.db[f'{collection}'].find_one({key: modelData[key]}):
                        Model.error('Validation error', f'{key} is already present in the database', 400)
    
    def checkValidators(Schema, modelData, skipField=[]):
        for key in Schema.keys():
            if key not in skipField:
                if 'validators' in Schema[key]:
                    for validator in Schema[key]['validators']:
                        #print(key, validator[0], validator[1])
                        getattr(Model, validator[0])(key, modelData, validator[1], schema=Schema)

    def validateInit(Schema, modelData, collection):
        Model.insertDefaults(Schema, modelData)
        Model.checkTypes(Schema, modelData)
        Model.checkRequired(Schema, modelData)
        Model.checkUnique(Schema, modelData, collection)
        Model.checkValidators(Schema, modelData, skipField=[])

    def validateUpdate(Schema, modelData, skip):
        modelData = Model.checkTypes(Schema, modelData)
        for key in modelData.keys():
            if((key in Schema.keys()) and (key not in skip)):
                if 'validators' in Schema[key].keys():
                    for validator in Schema[key]['validators']:
                        print(key, validator)
                        getattr(Model, validator[0])(key, modelData, validator[1])

    ####Error handler
    def error(errorType, msg, statusCode):
        response = jsonify({
            'status': errorType,
            'message': msg,
            'code': statusCode
            })
        response.status_code = statusCode
        return abort(response)

    ####Database functions#############

    ##Instance methods
    def save(self):
        preSaveHooks = [hook for hook in dir(self) if hook.startswith('_pre_save_')]
        for hook in preSaveHooks:
            getattr(self, hook)()
        mongo.db[f'{self.collection}'].insert_one(vars(self))
    
    ##Class methods
    @classmethod
    def filterRequestBody(cls, body, skip=[]):
        filteredObject = {}
        for key in body.keys():
            if key in cls.Schema.keys():
                if key not in skip:
                    filteredObject[key] = body[key]
        return filteredObject
    
    @classmethod
    def deleteOne(cls, query):
        return mongo.db[f'{cls.collection}'].delete_one(query)

    @classmethod
    def updateOne(cls, filter, newValues, validate=False, skip=[], returnNew = False, hideFields=['password']):

        if validate:
            for key in newValues:
                cls.validateUpdate(cls.Schema, newValues[key], skip)

        mongo.db[f'{cls.collection}'].update_one(filter, newValues)
        if returnNew:
            return cls.findOne(filter, hideFields=hideFields)
    
    @classmethod
    def findOne(cls, query, hideFields=['password']):
        
        result = mongo.db[f'{cls.collection}'].find_one(query)
        if not result: return None
        
        for key in hideFields:
            if key in result.keys():
                del result[key]

        return result
    
    @classmethod
    def find(cls, query, hideFields=['password']):
        results = [a for a in mongo.db[f'{cls.collection}'].find(query)]
        
        for r in results:
            for key in hideFields:
                if key in r.keys():
                    del r[key]

        return results
    
    @classmethod
    def populateField(cls, primary, populateField, model):
        primary[populateField]=model.findOne({'_id': primary[populateField]})
        return primary
        