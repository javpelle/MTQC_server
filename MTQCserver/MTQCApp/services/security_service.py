import hashlib
import time
import jwt

import datetime  

from MTQCApp.settings.settings import CRYPTO_KEY


def current_milli_time():
    return round(time.time() * 1000)


def generate_token(user_id: int, time: int = None):
    if time is None:
        time = int((datetime.datetime.now() + datetime.timedelta(days = 2)).timestamp())

    return jwt.encode({"user_id": user_id, "time": time}, CRYPTO_KEY, algorithm="HS256")

def validate_auth(auth_header: str):
    auth_list = auth_header.split(" ")

    if len(auth_list) >= 2 and auth_list[0] == "Bearer":
        token = auth_list[1]
        user_data = jwt.decode(token, CRYPTO_KEY, algorithms=["HS256"])
        date = datetime.datetime.fromtimestamp(user_data["time"])
        if (date >= datetime.datetime.now()):
            return user_data["user_id"]
        else:
            return None

    else:
        return None
