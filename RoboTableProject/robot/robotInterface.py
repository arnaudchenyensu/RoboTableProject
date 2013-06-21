# from RoboTableProject.robot.robotInterface import RobotInterface
# from RoboTableProject.tracking.sensorInterface import SensorInterface
import math
import time


class RobotInterface(object):
    """docstring for Robot"""

    def __init__(self, sensor):
        self.sensor = sensor
        self._front_led = {}
        self._back_left_led = {}
        self._back_right_led = {}
        # self._leds = {'front': self._front_led, 'left': self._back_left_led, 'right': self._back_right_led}

    @property
    def leds(self):
        leds_location = self.sensor.get_leds()
        self._determine_led_position(leds_location[0], leds_location[1], leds_location[2])
        return {'front': self._front_led, 'left': self._back_left_led, 'right': self._back_right_led}

    def _determine_led_position(self, led1, led2, led3):
        """determine led postion (e.g front_led, back_left_led and back_right_led)
        """
        dist_1_2 = self._get_distance_between_2_points(led1, led2)
        dist_2_3 = self._get_distance_between_2_points(led2, led3)
        dist_1_3 = self._get_distance_between_2_points(led1, led3)

        if math.fabs(dist_1_2) < math.fabs(dist_1_3):
            if math.fabs(dist_1_2) < math.fabs(dist_2_3):
                # Led 3 is the Front led
                self._front_led = led3
                self._determine_back_led_position(led1, led2, led3)
            else:
                # Led 1 is the Front led
                self._front_led = led1
                self._determine_back_led_position(led2, led3, led1)
        else:
            if (math.fabs(dist_1_3) < math.fabs(dist_2_3)):
                # Led 2 is the Front led
                self._front_led = led2
                self._determine_back_led_position(led1, led3, led2)
            else:
                # Led 1 is the Front led
                self._front_led = led1
                self._determine_back_led_position(led2, led3, led1)
        return([self._front_led, self._back_left_led, self._back_right_led])

    def _get_distance_between_2_points(self, led1, led2):
        """Return the distance between 2 points"""
        distX = led2["X"] - led1["X"]
        distY = led2["Y"] - led1["Y"]
        return math.sqrt((distX * distX) + (distY * distY))

    def _get_midpoint(self, led1, led2):
        """Return the midpoint between 2 points"""
        midX = (led1["X"] + led2["X"]) / 2
        midY = (led1["Y"] + led2["Y"]) / 2
        return {"X": midX, "Y": midY}

    def _determine_back_led_position(self, led1, led2, front_led):
        """determine back led position (e.g back_left_led and back_right_led)
        """
        midpoint = self._get_midpoint(led1, led2)
        if led1['X'] <= led2['X']:
            if midpoint['Y'] >= front_led['Y']:
                #point 1 is left and point 2 is right
                self._back_left_led = led1
                self._back_right_led = led2
            else:
                # point 2 is left and point 1 is right
                self._back_left_led = led2
                self._back_right_led = led1
        else:
            if midpoint['Y'] >= front_led['Y']:
                # point 2 is left and point 1 is right
                self._back_left_led = led2
                self._back_right_led = led1
            else:
                # point 1 is left and point 2 is right
                self._back_left_led = led1
                self._back_right_led = led2

    def show_leds(self):
        """ For testing purpose """
        while True:
            time.sleep(1)
            print(self.leds)
