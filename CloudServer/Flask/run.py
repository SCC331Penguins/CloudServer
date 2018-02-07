from flask import Flask
import config
from Flask.routes.user import user
from Flask.routes.sensor import sensor
from Flask.routes.router import router

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(sensor)
app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True, host=config.HOST, threaded=True)