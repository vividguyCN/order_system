from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import and_

app = Flask(__name__)

