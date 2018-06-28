"""Writing to graphite"""
import time
from datetime import datetime
import socket
from typing import Union

Num = Union[int, float]


class CarbonClient(object):

    def __init__(self, server: str, port: int = 2003):
        self.server = server
        self.port = port
        self.address = (self.server, self.port)

    def send(self, metric: str, timestamp: datetime, value: Num) -> None:
        unix_time = time.mktime(timestamp.timetuple())

        message = '{metric} {value} {timestamp}\n'.format(
            metric=metric,
            value=value,
            timestamp=unix_time
        ).encode('utf-8')

        print("Sending message: ", message)
        sock = socket.socket()
        sock.connect(self.address)
        sock.sendall(message)
        sock.close()
