from flask import Flask
import config

from Flask.routes.user import user
from Flask.routes.sensor import sensor
from Flask.routes.router import router
from Flask.routes.function import function
from Flask.routes.historic import historic
from Flask.routes.api import api

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(sensor)
app.register_blueprint(router)
app.register_blueprint(function)
app.register_blueprint(historic)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True, host=config.HOST, threaded=True)