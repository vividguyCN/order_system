from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return main.send_static_file("index.html")
