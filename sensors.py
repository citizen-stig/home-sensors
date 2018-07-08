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
