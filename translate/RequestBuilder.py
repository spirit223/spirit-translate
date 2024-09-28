import hashlib
import uuid
from datetime import datetime
import http.client
import urllib.parse

from translate.LanguageDiscriminator import LanguageDiscriminator
from translate.PreferencesInfo import PreferencesInfo


class RequestBuilder:
    sha256_hash = hashlib.sha256()

    @staticmethod
    def build(text:str, from_lan=None, to_lan=None, sign_type='v3'):
        url = "openapi.youdao.com"
        path = "/api"
        salt = RequestBuilder.build_slat()
        cur_time = int(datetime.now().timestamp())
        app_id = PreferencesInfo.app_id
        app_secret = PreferencesInfo.app_secrit
        if from_lan is None and to_lan is None:
            from_lan = LanguageDiscriminator.detect_language(text)
            if from_lan == 'zh-CHS':
                to_lan = 'en'
            else:
                to_lan = 'zh-CHS'
        elif from_lan == 'en':
            to_lan = 'zh-CHS'
        elif from_lan == 'zh-CHS':
            to_lan = 'en'

        data = {
            'q': text,
            'from': from_lan,
            'to': to_lan,
            'appKey': app_id,
            'salt': salt,
            'sign': RequestBuilder.build_sign(text, salt, cur_time, app_id, app_secret),
            'signType': sign_type,
            'curtime': cur_time
        }
        conn = http.client.HTTPSConnection(url)
        encoded_data = urllib.parse.urlencode(data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn.request("POST", path, encoded_data, headers)
        response = conn.getresponse()
        response_data = response.read().decode()
        conn.close()
        return Response(response.status, response_data)

    @staticmethod
    def get_input_str(text:str):
        q_len = len(text)
        if q_len > 20:
            return text[:10] + str(q_len) + text[10:]
        else:
            return text

    @staticmethod
    def build_slat():
        return str(uuid.uuid1().int)

    @staticmethod
    def build_sign(text: str, salt:str, cur_time: int, app_id:str, app_secret:str):
        input_str = RequestBuilder.get_input_str(text)
        print("text is [%s]" % text)
        print("input_str is [%s]" % input_str)
        print("salt is [%s]" % salt)
        print("cur_time is [%s]" % str(cur_time))
        print("app_id is [%s]" % str(app_id))
        print("app_secret is [%s]" % str(app_secret))

        RequestBuilder.sha256_hash.update(str(app_id + input_str + str(salt) + str(cur_time) + app_secret).encode('utf-8'))
        return RequestBuilder.sha256_hash.hexdigest()

class Response:
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data