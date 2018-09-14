import configparser
import os
from pathlib import Path
import sys


def get_config() -> configparser.ConfigParser:
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'config.ini'
    )
    if not Path(config_path):
        sys.stderr.write('Cannot open config {}'.format(config_path))
        raise FileNotFoundError

    config = configparser.ConfigParser()
    config.read(config_path)

    return config
