import datetime
import sqlite3
import config
import time
from Database.dbhandler import DbHandler
from Authentication import authenticator

class HistoricHandler:

    def __init__(self):
        self.connection = sqlite3.connect(config.HISTORIC_DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def record_reading(self, timestamp, router_id, data):
        print(data['id'])
        sensor_id=data['id']
        temperature=data['temperature']
        humidity=data['humidity']
        movement=data['movement']
        light=data['light']
        sound=data['sound']
        uv=data['uv']
        ir=data['ir']

        if temperature != "null":
            self.execute_query("INSERT INTO temperature" 
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(temperature)+")")
        if humidity != "null":
            self.execute_query("INSERT INTO humidity" 
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(humidity)+")")
        if light != "null":
            self.execute_query("INSERT INTO light"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(light)+")")
        if movement != "null":
            self.execute_query("INSERT INTO movement"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(movement)+")")
        if sound != "null":
            self.execute_query("INSERT INTO sound"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(sound)+")")
        if uv != "null":
            self.execute_query("INSERT INTO uv"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(uv)+")")
        if ir != "null":
            self.execute_query("INSERT INTO ir"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(ir)+")")

    def get_reading(self, router_id, sensor_id=None):
        if sensor_id == None:
            pass

        data = {}
        result = {}
        list = []
        #TODO: Time between dates
        temperature = self.fetch_result(self.execute_query("SELECT timestamp, value FROM temperature WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"temperature":temperature})
        humidity = self.fetch_result(self.execute_query("SELECT timestamp, value FROM humidity WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"humidity":humidity})
        light = self.fetch_result(self.execute_query("SELECT timestamp, value FROM light WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"light":light})
        movement = self.fetch_result(self.execute_query("SELECT timestamp, value FROM movement WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"movement":movement})
        sound = self.fetch_result(self.execute_query("SELECT timestamp, value FROM sound WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"sound":sound})
        uv = self.fetch_result(self.execute_query("SELECT timestamp, value FROM uv WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"uv":uv})
        ir = self.fetch_result(self.execute_query("SELECT timestamp, value FROM ir WHERE sensor_id = '"+str(sensor_id)+"'"))
        data.update({"ir":ir})
        list.append(data)
        result.update({"data":list})
        return result


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
        self.connection.commit()

    def close(self):
        self.cursor = None
        self.connection.close()

    @staticmethod
    def fetch_result(result):
        result_array = []
        while True:
            fetched_result = result.fetchone()
            if fetched_result is None:
                break
            result_array.append(fetched_result)
        return result_array