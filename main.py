import configparser

import sensors
from carbon_client import CarbonClient
from ssh import SSHTunnelWrapper


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    carbon_host = config.get('carbon', 'host')
    carbon_port = int(config.get('carbon', 'port'))
    prefix = config.get('carbon', 'prefix')

    ssh_host = config.get('ssh', 'host')
    ssh_user = config.get('ssh', 'user')
    ssh_key = config.get('ssh', 'pkey')
    print('ssh -i {} {}@{}'.format(ssh_key, ssh_user, ssh_host))

    carbon_ssh_client = SSHTunnelWrapper(
        ssh_host=ssh_host,
        ssh_key_path=ssh_key,
        username=ssh_user,
        remote_host=carbon_host,
        remote_port=carbon_port,
        sender_class=CarbonClient,
    )

    # Temperature and humidity
    ht_pin = int(config.get('sensors', 'ht_pin'))
    ht_timestamp, humidity, temperature = sensors.get_humidity_and_temperature(ht_pin)

    carbon_ssh_client.send(prefix + '.temperature', ht_timestamp, temperature)
    carbon_ssh_client.send(prefix + '.humidity', ht_timestamp, humidity)

    # Noise

    # Dust


    # for sensor_name, get_sensor_value in available_sensors:
    #     timestamp, value = get_sensor_value()
    #     metric = prefix + '.' + sensor_name
    #     print(timestamp, metric, value)
    #     # carbon_client.send(metric, timestamp,  value)
    #     carbon_ssh_client.send(metric, timestamp, value)


if __name__ == '__main__':
    main()
