from flask import Flask
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)