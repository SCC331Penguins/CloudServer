from flask import Flask
import config
from Flask.routes.user import user
from Flask.routes.sensor import sensor

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(sensor)

if __name__ == '__main__':
    app.run(debug=True, host=config.HOST, threaded=True)