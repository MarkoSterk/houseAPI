from xmlrpc.client import Boolean
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

collection = 'user' <-- the desired collection in MongoDB
"""

class User(Model):
    collection = 'user'

    hideFields = ['_v', '_createdAt', '_active']

    Schema = {
        'name': {
            'type': str,
            'validators': [
                ('minLength', 9),
                ('maxLength', 25)
            ],
            'required': True
        },
        'email': {
            'type': str,
            'validators': [
                ('isEmail', True)
            ],
            'required': True,
            'unique': True
        },
        'password': {
            'type': str,
            'validators': [
                ('minLength', 8),
                ('mustMatch', 'passwordConfirm')
            ],
            'required': True
        },
        'active': {
            'type': Boolean,
            'required': True,
            'default': True
        },
        'role': {
            'type': str,
            'required': True,
            'default': 'user'
        },
        'passwordChangedAt': {
            'type': str,
            'required': False
        }
    }
    
    def __init__(self, user):
        #super().__init__(user)
        Model.__init__(self, user)
    
    def _pre_save_hashpw(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')

        