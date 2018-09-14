from config import get_config
from sensors import read_sensors_data
from carbon_client import send_to_carbon


def main():
    config = get_config()

    data = read_sensors_data(config)
    send_to_carbon(config, data)


if __name__ == '__main__':
    main()
