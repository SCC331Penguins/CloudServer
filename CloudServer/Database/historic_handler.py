import datetime
import sqlite3
import config
import time
from Authentication import authenticator

class HistoricHandler:

    def __init__(self):
        self.connection = sqlite3.connect(config.HISTORIC_DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def record_reading(self, timestamp, router_id, data):
        sensor_id=data['id']
        temperature=data['temperature']
        humidity=data['humidity']
        light=data['light']
        if temperature != "null":
            self.execute_query("INSERT INTO temperature" 
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(temperature)+")")
        if humidity != "null":
            self.execute_query("INSERT INTO humidity" 
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(humidity)+")")
        if light != "null":
            self.execute_query("INSERT INTO light"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(light)+")")

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