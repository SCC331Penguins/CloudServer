import datetime
import sqlite3
import config
import time
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from Authentication import authenticator
from flask import jsonify

class DbHandler:

    def __init__(self):
        self.connection = sqlite3.connect(config.DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def verify_router(self, token):
        router = authenticator.verify_token(token)
        result = self.fetch_result(self.execute_query("SELECT router_id FROM Routers WHERE router_id = '" + str(router) +"'"))
        if len(result) == 0:
            return False
        return router

    def set_sensor_mode(self, sensor_id, config):
        self.execute_query("UPDATE Sensor SET sensor_settings = " + str(config) + " WHERE sensor_id = '" + str(sensor_id) + "'")

    def get_router_status(self,router_id):
        result = self.fetch_result(self.execute_query("SELECT last_heard FROM Routers WHERE router_id = '" + str(router_id) +"';"))[0][0]
        time_now = int(time.time())
        if (time_now - result) < 120:
            return True
        return False

    def create_user(self, username, password):
        password_hash = pwd_context.encrypt(password)
        createUserQuery = "INSERT INTO Users (username, password) VALUES('" + username + "', '" + password_hash + "')"
        if len(self.retreive_user(username)) >= 1:
            return {'result':False, 'message':"Username already exists"}
        self.execute_query(createUserQuery)
        return {'result': True, 'message': "Username created"}

    def retreive_user(self, username):
        return self.fetch_result(self.execute_query("SELECT * FROM Users WHERE username = '" + username + "';"))

    def get_users_router(self, token):
        user_id = authenticator.verify_token(token)
        if user_id == None:
            return None
        print(user_id)
        result = self.fetch_result(self.execute_query("SELECT router_id FROM UserRouters WHERE user_id = " + str(user_id) +""))
        return_result = []
        for x in result[:]:
            time = self.get_router_status(x[0])
            x = x + (time,)
            return_result.append(x)
        return return_result

    def login_user(self, username, password):
        result = self.retreive_user(username)
        if len(result) == 0:
            return [(False, "Username does not exist")]
        if pwd_context.verify(password, result[0][2]) == True:
            return [(True, authenticator.generate_token(result[0][0]))]
        self.record_error(config.ERROR_LOGIN_ATTEMPT, "Attempt login on user: " + str(username))
        return [(False, "Incorrect password")]

    def update_router_status(self, router_id):
        self.execute_query("UPDATE Routers SET last_heard = "+ str(int(time.time())) +" WHERE router_id = '"+str(router_id)+"';")

    def register_router(self, user_id, router_id):
        router = self.retreive_router(router_id)
        if len(router) == 0:
            self.record_error(config.ERROR_INVALID_ROUTER, "User attempted: " + str(user_id) + ", router does not exist: " + str(router_id) )
            return "Router not found"
        registerQuery = "INSERT INTO UserRouters (user_id, router_id) VALUES ( '" + str(user_id) +"', '" + str(router_id) + "' )"
        print(registerQuery)
        result = self.execute_query(registerQuery)
        if result == 0:
            self.record_error(config.ERROR_INVALID_ROUTER, "router already registered: " + str(router_id))
            return "router already registered"
        return "router registered"

    def retreive_router(self, router_id):
        return self.fetch_result(self.execute_query("SELECT router_id FROM Routers WHERE router_id = '"+router_id+"'"))

    def get_router_channels(self):
        return self.fetch_result(self.execute_query("SELECT router_id FROM Routers"))

    def init_sensor(self, sensor_id, router_id):
        checkSensorExists = "SELECT sensor_id FROM Sensor WHERE sensor_id = '" + str(sensor_id) + "';"
        result = self.fetch_result(self.execute_query(checkSensorExists))
        if len(result) == 0:
            self.record_error(config.ERROR_INVALID_SENSOR, "Router " + str(router_id) + " tried to register sensor: " + str(sensor_id) + ", does not exist")
            return "sensor does not exist"
        findSensor = "SELECT sensor_id FROM RouterSensors WHERE sensor_id = '" + str(sensor_id) + "';"
        result = self.fetch_result(self.execute_query(findSensor))
        if len(result) >= 1:
            initSensorQuery = "UPDATE RouterSensors SET router_id = '" + str(router_id) + "' WHERE sensor_id = '" + str(sensor_id) + "';"
            print("Updating sensors router")
        else:
            initSensorQuery = "INSERT INTO RouterSensors (sensor_id, router_id) VALUES ('" + str(sensor_id) + "', '" + str(router_id) + "');"
            print("Adding sensors router")
        self.execute_query(initSensorQuery)

    def get_router_sensors(self, router_id):
        findRouterSensor = "SELECT RouterSensors.sensor_id, Sensor.sensor_settings FROM RouterSensors INNER JOIN Sensor ON Sensor.sensor_id = RouterSensors.sensor_id WHERE RouterSensors.router_id = '" + str(router_id) + "';"
        result = self.fetch_result(self.execute_query(findRouterSensor))
        return result

    def update_phone_token(self, user_id, token):
        routers = self.get_users_router(user_id)
        for x in routers[:]:
            router_id = x[0]
            checkToken = "SELECT router_id FROM NotificationTokens WHERE router_id = '"+str(router_id)+"'"
            update = "UPDATE NotificationTokens SET token = '"+str(token)+"' WHERE router_id = '"+str(router_id)+"'"
            tokenQuery = "INSERT INTO NotificationTokens VALUES ('"+str(router_id)+"', '"+str(token)+"')"

            result = self.fetch_result(self.execute_query(checkToken))
            if len(result) >= 1:
                self.execute_query(update)
            else:
                self.execute_query(tokenQuery)

    def get_phone_token(self, router_id):
        return self.fetch_result(self.execute_query("SELECT token FROM NotificationTokens WHERE router_id = '"+str(router_id)+"'"))

    def check_admin(self, username):
        adminQuery = "SELECT is_admin FROM Users WHERE username = '" + str(username) + "';"
        result = self.fetch_result(self.execute_query(adminQuery))[0][0]
        if result == False:
            self.record_error(config.ERROR_UNAUTHORISED_ACCESS, "User " + str(username) + ", tried to access admin domain")
        return True if result == 1 else False

    #TODO: Record Errors in Database
    def record_error(self, error_type, error_message):
        errorQuery = "INSERT INTO Errors (timestamp, error_type, error_message) VALUES ('" + str(datetime.datetime.utcnow()) + "', '" + str(error_type) + "', '" + str(error_message) + "');"
        print(errorQuery)
        self.execute_query(errorQuery)
        return

    def get_script(self, router_id):
        return self.fetch_result(self.execute_query("SELECT script FROM Scripts WHERE router_id = '"+str(router_id)+"'"))

    def record_script(self, router_id, script):
        router = self.retreive_router(router_id)
        if len(router) == 0:
            return
        self.execute_query("INSERT INTO Scripts (router_id, script) VALUES ('"+str(router_id)+"', '"+str(script)+"')")
        return

    def set_actuator(self, router_id, actuator_id, actuator_type):
        result = self.fetch_result(self.execute_query("SELECT * FROM Actuators WHERE actuator_id = '"+str(actuator_id)+"'"))
        if len(result) >= 1:
            self.execute_query("UPDATE Actuators SET router_id = '"+str(router_id)+"', type = '"+str(actuator_id)+"' WHERE actuator_id = '"+str(actuator_id)+"'")
        else:
            self.execute_query("INSERT INTO Actuators VALUES ('"+str(actuator_id)+"','"+str(router_id)+"','"+str(actuator_type)+"')")

    def get_actuators(self, router_id):
        return self.fetch_result(self.execute_query("SELECT actuator_id, type FROM Actuators WHERE router_id = '"+str(router_id)+"'"))

    def execute_query(self, query):
        result = []
        try:
            result = self.cursor.execute(query)
        except Exception as e:
            print (e)
            result = 0
        self.save()
        return result

    def save(self):
        """
        Saves the database after successful insertion/deletion
        """
        self.connection.commit()

    def close(self):
        """
        Closes db connection
        """
        self.cursor = None
        self.connection.close()

    @staticmethod
    def fetch_result(result):
        """
        Fetch query result into a python array.
        :param result: query result
        :return: result array
        """
        result_array = []
        while True:
            fetched_result = result.fetchone()
            if fetched_result is None:
                break
            result_array.append(fetched_result)
        return result_array