import sqlite3
import config
import time
from WAMP import packet
from Handlers import message_handler

class ChangeHandler:

    def __init__(self,WAMP):
        self.connection = sqlite3.connect(config.CHANGE_DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.WAMP = WAMP

    def check_changes(self):
        while(True):
            result = self.fetch_result(self.execute_query("SELECT * FROM Changes"))
            if len(result) != 0:
                for x in result[:]:
                    self.handle_changes(x[0], x[1])
                pass
            time.sleep(1)

    def handle_changes(self, id, type):
        if type == packet.Type.UPDATE_SENSORS:
            packet_to_send = message_handler.update_sensors(id)
            self.WAMP.sendEvent(id, packet_to_send)
        elif type == packet.Type.OPEN_SOCKET:
            self.WAMP.openPhoneSocket(id)
        self.execute_query("DELETE FROM Changes WHERE id = '" + str(id) + "' AND type = " + str(type) + ";")

    def new_change(self, id, type):
        self.execute_query("INSERT INTO Changes VALUES('" + str(id) +"', " + str(type) + ")")

    def socket_change(self, uniqueid, type):
        self.execute_query("INSERT INTO Changes VALUES('" + str(uniqueid) + "', " + str(type) + ")")

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