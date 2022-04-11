from xmlrpc.client import Boolean
from .model import Model
from app import bcrypt

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

        