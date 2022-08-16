from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import Library, User
import os
SECRET_KEY = os.environ.get('CT_SECRET_KEY')

def user_token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            current_user_token = User.query.filter_by(user_token = token).first()
            
        except:
            owner = User.query.filter_by(usertoken = token).first()
            
            if token != owner.token and secrets.compare_digest(token, owner.user_token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

def library_token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            current_library_token = Library.query.filter_by(library_token = token).first()
            
        except:
            owner = Library.query.filter_by(token = token).first()
            
            if token != owner.library_token and secrets.compare_digest(token, owner._library_token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_library_token, *args, **kwargs)
    return decorated

def secret_key_required(our_flask_funciton):
    @wraps(our_flask_funciton)
    def decorated(*args, **kwargs):
        current_secret_key = None
        
        if 'x-access-token' in request.headers:
            current_secret_key = request.headers['x-access-token'].split(' ')[1]
        if not current_secret_key:
            return jsonify({'message': 'Token is missing'}), 401
    
        print(current_secret_key)
        print(SECRET_KEY)
        if current_secret_key != SECRET_KEY:
            return jsonify({'message': 'Token is invalid'})
        return our_flask_funciton(current_secret_key, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)