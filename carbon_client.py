"""Writing to graphite"""
import time
import configparser
from datetime import datetime
import socket
import random
from typing import Union

from ssh import SSHTunnelWrapper

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

        sock = socket.socket()
        sock.connect(self.address)
        sock.sendall(message)
        sock.close()


def send_to_carbon(config: configparser.ConfigParser, data: dict) -> None:
    carbon_host = config.get('carbon', 'host')
    carbon_port = int(config.get('carbon', 'port'))

    ssh_host = config.get('ssh', 'host')
    ssh_user = config.get('ssh', 'user')
    ssh_key = config.get('ssh', 'pkey')

    carbon_ssh_client = SSHTunnelWrapper(
        ssh_host=ssh_host,
        ssh_key_path=ssh_key,
        username=ssh_user,
        remote_host=carbon_host,
        remote_port=carbon_port,
        sender_class=CarbonClient
    )
    for metric, item in data.items():
        timestamp, value = item
        carbon_ssh_client.send(metric, timestamp, value)
        time.sleep(1)

    carbon_ssh_client.stop()


def self_check():
    config = configparser.ConfigParser()
    config.read('config.ini')
    prefix = config.get('carbon', 'prefix')
    sample_data = {
        prefix + '.' + k: (datetime.now(), random.randint(0, 50))
        for k in ('check1', 'check2')
    }
    print(sample_data)
    send_to_carbon(config, sample_data)


if __name__ == '__main__':
    self_check()
