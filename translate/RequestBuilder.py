import hashlib
import uuid
import time


class RequestBuilder:
    @staticmethod
    def build_slat():
        return uuid.uuid1()

    @staticmethod
    def build(text):
        app_id = ''
        app_secret = ''
        input_str = ''
        salt = RequestBuilder.build_slat()
        cur_time = time.time()

        return ''