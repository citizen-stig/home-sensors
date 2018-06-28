import getpass
import socket
from contextlib import closing

import sshtunnel


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


class SSHTunnelWrapper(object):

    def __init__(self,
                 ssh_host: str,
                 ssh_key_path: str,
                 remote_host: str,
                 remote_port: int,
                 sender_class: callable,
                 ssh_port: int = 22,
                 username: str = None):
        self.ssh_address = (ssh_host, ssh_port)
        self.username = username if username is not None else getpass.getuser()
        self.ssh_key_path = ssh_key_path
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_bind_address = 'localhost'
        self.local_port = find_free_port()
        self.sender = sender_class(server=self.local_bind_address, port=self.local_port)

    def send(self, *args, **kwargs):
        with sshtunnel.SSHTunnelForwarder(
                self.ssh_address,
                ssh_username=self.username,
                ssh_pkey=self.ssh_key_path,
                remote_bind_address=(self.remote_host, self.remote_port),
                local_bind_address=(self.local_bind_address, self.local_port)
        ):
            self.sender.send(*args, **kwargs)