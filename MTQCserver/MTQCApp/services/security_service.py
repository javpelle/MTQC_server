import hashlib
import time


def current_milli_time():
    return round(time.time() * 1000)


def generate_token(msg: str, time: int = None):
    if time == None:
        time = current_milli_time()
    token_msg = msg + str(time)
    return hashlib.sha256(token_msg.encode('utf-8')).hexdigest()
