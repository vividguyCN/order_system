from flask import Blueprint

main = Blueprint('main', __name__, static_url_path='/view/static', static_folder='static')


@main.route('/')
def index():
    print(main.static_url_path)
    print(main.static_folder)
    return main.send_static_file("index.html")
