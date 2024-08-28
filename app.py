import logging
from server.redis_instance import r
from server.config import thread_number
from chatbot.worker import ThreadPool
import json
from chatbot.utils import handler
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':

    pool = ThreadPool(thread_number)

    while True:
        try:
            packed = r.blpop(['telle:queue:bot'], 30)

            if not packed:
                continue

            message = json.loads(packed[1])

            print('From telle:queue:bot {}'.format(message))

            func_name = message['type']
            group_id = message['groupId']
            tid = ord(group_id[-1]) % thread_number
            if func_name in handler:
                pool.map(tid, handler[func_name], [message])

            time.sleep(0.5)
        except Exception as e:
            print(e)
            logger.info(e)
            continue
