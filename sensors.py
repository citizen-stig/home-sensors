import configparser
from datetime import datetime
from typing import Tuple
import atexit
import time

import Adafruit_DHT
import grovepi


def get_humidity_and_temperature(pin: int) -> Tuple[datetime, float, float]:
    timestamp = datetime.now()
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)
    return timestamp, humidity, temperature


def get_noise(pin: int) -> Tuple[datetime, int]:
    grovepi.pinMode(pin, 'INPUT')
    timestamp = datetime.now()
    values = []
    samples = 5
    for i in range(samples):
        value = grovepi.analogRead(pin)
        values.append(value)
        time.sleep(0.1)
    avg_value = int(round(sum(values) / samples))
    return timestamp, avg_value


def get_dust() -> Tuple[datetime, int]:
    atexit.register(grovepi.dust_sensor_dis)
    grovepi.dust_sensor_en()
    attempts = 100
    for _ in range(attempts):
        timestamp = datetime.now()
        new_val, low_pulse_occupancy = grovepi.dustSensorRead()
        if new_val:
            return timestamp, low_pulse_occupancy
        time.sleep(3)
    else:
        raise ValueError('Cannot read values from dust sensor')


def read_sensors_data(config: configparser.ConfigParser) -> dict:
    data = {}
    prefix = config.get('carbon', 'prefix')

    # Humidity and Temperature
    humidity_and_temperature_pin = int(
        config.get('sensors', 'humidity_and_temperature_pin'))
    timestamp, humidity, temperature = get_humidity_and_temperature(
        humidity_and_temperature_pin)
    data[prefix + '.temperature'] = (timestamp, temperature)
    data[prefix + '.humidity'] = (timestamp, humidity)

    # Noise
    sound_pin = int(
        config.get('sensors', 'sound_pin'))
    timestamp, noise = get_noise(sound_pin)
    data[prefix + '.noise'] = (timestamp, noise)

    # Dust
    try:
        timestamp, dust = get_dust()
        data[prefix + '.dust'] = (timestamp, dust)
    except ValueError:
        pass

    return data


def self_check():
    config = configparser.ConfigParser()
    config.read('config.ini')
    data = read_sensors_data(config)
    print(data)


if __name__ == '__main__':
    self_check()
