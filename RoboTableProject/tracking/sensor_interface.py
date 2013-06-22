import cwiid
import time

wii = 0


class SensorInterface(object):
    """Simple Interface to inherit (or implement) for a new sensor"""

    def __init__(self):
        self.connect()

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_leds(self):
        pass
