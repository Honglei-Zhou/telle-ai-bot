import redis

from .tools import get_time, get_uuid


class MessageQueue(object):

    def __init__(self, conn, queue='queue', ack_queue='ack_queue'):
        self._conn = conn
        self.set_queue(queue, ack_queue)

    def set_queue(self, queue, ack_queue):
        self.queue = queue
        self.ack_queue = ack_queue

    def rpush(self, msg, timeout=0):
        self._conn.rpush(self.queue, msg)
        if timeout:
            msg = "{}{}".format(msg, get_uuid())
            self.zadd(get_time() + timeout, msg)
            return msg
        return True

    def commit(self, msg):
        return self.zrem(msg)

    def lpop(self):
        msg = self._conn.lpop(self.queue)
        return msg

    def zadd(self, timestamp, value):
        return self._conn.zadd(self.ack_queue, value, timestamp)

    def zrem(self, value):
        return self._conn.zrem(self.ack_queue, value)

    def zscore(self, value):
        return self._conn.zscore(self.ack_queue, value)

    def zrangebyscore(self):
        res = self._conn.zrangebyscore(self.ack_queue, 0, get_time())
        if not isinstance(res, list):
            res = [res]
        return res
