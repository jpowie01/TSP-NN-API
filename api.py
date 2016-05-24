from flask import Flask
from flask.ext.restplus import Api


app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api = Api(app, version='1.0', title='AI API', description='A simple API for AI class project')

tsp = api.namespace('tsp', description='TSP API')
