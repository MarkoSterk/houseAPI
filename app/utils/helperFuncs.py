from app import bcrypt
import secrets
from flask import current_app
import os
from werkzeug.utils import secure_filename

"""
Helper functions which can be used across the app. 

hashUrlSafe: creates a URL safe hashed string

parseFormData: turns form data (immutableDict) into a normal dictionary. Can be set to skip 
desired fields.

saveImageFiles: saves image files from a form into the static folder and asignes
random string names (it keeps the provided extension) but it only accepts provided
image formats (allowed_formats). Default: allowed_formats=['png', 'jpg', 'jpeg', 'bmp']
"""

def hashUrlSafe(stringToHash):
    hashed_string = '/'
    while True:
        if '/' in hashed_string:
            hashed_string = bcrypt.generate_password_hash(str(stringToHash)).decode('utf-8')
        else:
            break
        
    return hashed_string


def parseFormData(formData, skip=[]):
    parsedForm={}
    for key in formData.keys():
        if key not in skip:
            parsedForm[key]=formData[key]
    
    return parsedForm


def saveImageFiles(files, allowed_formats=['png', 'jpg', 'jpeg', 'bmp']):
    fileNames = []
    for file in files:
        ext = file.filename.split('.')[-1]
        if ext in allowed_formats:
            #fileName = secure_filename(file.filename)
            fileName = secrets.token_hex(16) + '.' + ext
            filePath=os.path.join(current_app.root_path, 'static', fileName)
            file.save(filePath)
            fileNames.append(fileName)
    return fileNames