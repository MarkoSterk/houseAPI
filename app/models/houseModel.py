from xmlrpc.client import Boolean, boolean
from .model import Model
from app import bcrypt

"""
Schema of the model object. A dictionary (Schema) with keys corresponding to field names.
Each field in the Schema is a dictionary with "type", "unique", "required", "default" and "validators" fields.
type: datatype(str, int, float, list ect...)
validators: a list of tuples with names and parameters (see model.py and example below)
"required": boolean (True or False)
"unique": boolean (True or False). Automatically checks the DB for existing value
"default": default value for the field if non is provided.

collection = 'house' <-- the desired collection in MongoDB
"""

class House(Model):
    collection = 'house'

    Schema = {
        'title': {
            'type': str,
            'validators': [
                ('minLength', 10),
                ('maxLength', 100)
            ],
            'required': True
        },
        'price': {
            'type': (int, float),
            'validators': [
                ('minValue', 0.0)
            ],
            'required': True
        },
        'bedrooms': {
            'type': (int, float),
            'validators': [
                ('minValue', 0)
            ]
        },
        'bathrooms': {
            'type': (int, float),
            'validators': [
                ('minValue', 0)
            ]
        },
        'sqft_living': {
            'type': (int, float),
            'validators': [
                ('minValue', 0)
            ],
            'required': True
        },
        'sqft_lot': {
            'type': (int, float),
            'validators': [
                ('minValue', 0)
            ],
            'required': True
        },
        'floors': {
            'type': (int, float),
            'required': False,
            'validators': [
                ('minValue', 1)
            ],
            'default': 1
        },
        'waterfront': {
            'type': Boolean,
            'required': True,
            'default': False
        },
        'condition': {
            'type': (int, float),
            'required': True,
            'validators': [
                ('minValue', 1),
                ('maxValue', 10)
            ],
            'default': 5
        },
        'coordinates': {
            'type': list,
            'required': True,
            'default': [47.5, -122.1],
            'validators': [
                ('checkElementsType', (int, float)),
                ('isLength', 2)
            ]
        },
        'description': {
            'type': str,
            'required': False
        },
        'coverImage': {
            'type': str,
            'required': True,
            'default': 'houseCover.jpg'
        },
        'images' :{
            'type': (list, boolean),
            'validators': [
                ('checkElementsType', str)
            ],
            'default': []
        },
        'seller': {
            'type': str,
            'required': True
        }
    }
    
    def __init__(self, user):
        #super().__init__(user)
        Model.__init__(self, user)

