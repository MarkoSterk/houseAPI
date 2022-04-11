from xmlrpc.client import Boolean, boolean
from .model import Model
from app import bcrypt
from .userModel import User

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

