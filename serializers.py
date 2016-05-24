from flask.ext.restplus import fields

from api import api


point_model = api.model('Point', {
    'id': fields.Integer,
    'x': fields.Float,
    'y': fields.Float
})

tsp_model_input = api.model('TSP', {
    'graph': fields.Nested(point_model, description='List of graph points')
})

tsp_model_output = api.model('TSP', {
    'expected': fields.List(fields.List(fields.Float), description='Two dimensional array with data'),
    'net': fields.List(fields.List(fields.Float), description='Two dimensional array with data'),
    'expected_order': fields.List(fields.Integer, description='Expected order of points'),
    'net_order': fields.List(fields.Integer, description='Order of points')
})
