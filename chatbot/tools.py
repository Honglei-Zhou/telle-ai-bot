import uuid
import time


def get_uuid():
    return uuid.uuid4().hex


def get_time():
    return int(time.time())
