from order_system.app import create_app
from order_system.app.common import db
import os


config_name = os.environ.get('FLASK_ENV') or 'default'

app = create_app(config_name)
db.init_app(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=False)
