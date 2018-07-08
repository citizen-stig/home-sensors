import configparser

import sensors
from carbon_client import CarbonClient
from ssh import SSHTunnelWrapper


def read_sensors_data(config: configparser.ConfigParser) -> dict:
    data = {}
    prefix = config.get('carbon', 'prefix')

    # Humidity and Temperature
    humidity_and_temperature_pin = int(
        config.get('sensors', 'humidity_and_temperature_pin'))
    timestamp, humidity, temperature = sensors.get_humidity_and_temperature(
        humidity_and_temperature_pin)
    data[prefix + '.temperature'] = (timestamp, temperature)
    data[prefix + '.humidity'] = (timestamp, humidity)

    # Noise
    sound_pin = int(
        config.get('sensors', 'sound_pin'))
    timestamp, noise = sensors.get_noise(sound_pin)
    data[prefix + '.noise'] = (timestamp, noise)

    # Dust
    try:
        timestamp, dust = sensors.get_dust()
        data[prefix + '.dust'] = (timestamp, dust)
    except ValueError:
        pass

    return data


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
        sender_class=CarbonClient,
    )

    for metric, item in data.items():
        timestamp, value = item
        carbon_ssh_client.send(metric, timestamp, value)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    data = read_sensors_data(config)
    print(data)


if __name__ == '__main__':
    main()
