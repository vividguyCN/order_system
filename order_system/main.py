from app import create_app
from app.common import db
import os


config_name = os.environ.get('FLASK_ENV') or 'default'

app = create_app(config_name)
db.init_app(app)


@app.route('/')
def index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
