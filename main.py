from datetime import datetime
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

    available_sensors = [
        (x.replace('get_', ''), getattr(sensors, x))
        for x in dir(sensors)
        if x.startswith('get_')
    ]
    for sensor_name, get_sensor_value in available_sensors:
        value = get_sensor_value()
        metric = prefix + '.' + sensor_name
        timestamp = datetime.utcnow()
        print(timestamp, metric, value)
        # carbon_client.send(metric, timestamp, value)
        carbon_ssh_client.send(metric, timestamp, value)


if __name__ == '__main__':
    main()
