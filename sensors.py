import Adafruit_DHT
from datetime import datetime
import random
from typing import Tuple


def get_humidity_and_temperature(pin: int) -> Tuple[datetime, float, float]:
    timestamp = datetime.utcnow()
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)
    return timestamp, humidity, temperature


def get_noise():
    return random.randint(1, 30)
