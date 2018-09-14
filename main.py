import configparser

from sensors import read_sensors_data
from carbon_client import send_to_carbon


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    data = read_sensors_data(config)
    send_to_carbon(config, data)


if __name__ == '__main__':
    main()
