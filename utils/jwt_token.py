import jwt
import datetime
from odoo.http import request

def get_secret():
    return request.env['ir.config_parameter'].sudo().get_param('jwt_secret', 'default_secret')

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, get_secret(), algorithm='HS256')

def verify_token(token):
    try:
        jwt.decode(token, get_secret(), algorithms=["HS256"])
        return True
    except:
        return False
