from flask_restx import fields
from app import api


realty_model = api.model('Realty', {
    'id': fields.Integer(required=True, description='ID'),
    'title': fields.String(required=True, description='Name'),
    'price': fields.Integer(required=True, description='Price'),
    'city': fields.String(required=True, description='City')
})
