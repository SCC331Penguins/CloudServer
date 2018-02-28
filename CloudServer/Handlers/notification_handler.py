from pyfcm import FCMNotification
from Database.dbhandler import DbHandler
import config

def send_notification(router_id, data_message):
    print(data_message['message'])
    push_service = FCMNotification(api_key=config.FCM_SERVER_API)
    db = DbHandler()
    token = db.get_phone_token(router_id)[0][0]
    result = push_service.notify_single_device(registration_id=token,data_message=data_message)
    print(result)