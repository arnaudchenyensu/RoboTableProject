import math


class RobotInterface(object):
    """docstring for Robot"""

    def __init__(self):
        self.front_led = {}
        self.back_left_led = {}
        self.back_right_led = {}

    #TODO
    @property
    def front_led(self):
        leds = sensor.getLEDS()
        self._determine_LED_position(leds[0], leds[1], leds[2])
        return self._front_led

    def get_location(self):
        pass

    def _determine_LED_position(self, led1, led2, led3):
        """determine LED postion (e.g front_led, back_right_led and back_left_led)
        """
        dist_1_2 = self._distance_between_2_points(led1, led2)
        dist_2_3 = self._distance_between_2_points(led2, led3)
        dist_1_3 = self._distance_between_2_points(led1, led3)

        if math.fabs(dist_1_2) < math.fabs(dist_1_3):
            if math.fabs(dist_1_2) < math.fabs(dist_2_3):
                # Led 3 is the Front LED
                self.front_led = led3
                self._determine_back_LED_position(led1, led2, led3)
            else:
                # Led 1 is the Front LED
                self.front_led = led1
                self._determine_back_LED_position(led2, led3, led1)
        else:
            if (math.fabs(dist_1_3) < math.fabs(dist_2_3)):
                # Led 2 is the Front LED
                self.front_led = led2
                self._determine_back_LED_position(led1, led3, led2)
            else:
                # Led 1 is the Front LED
                self.front_led = led1
                self._determine_back_LED_position(led2, led3, led1)

    def _distance_between_2_points(self, led1, led2):
        """Return the distance between 2 points"""
        distX = led2["X"] - led1["X"]
        distY = led2["Y"] - led1["Y"]
        return math.sqrt((distX * distX) + (distY * distY))

    def _midpoint(self, led1, led2):
        """Return the midpoint between 2 points"""
        midX = (led1["X"] + led2["X"]) / 2
        midY = (led1["Y"] + led2["Y"]) / 2
        return {"X": midX, "Y": midY}

    def _determine_back_LED_position(self, led1, led2, front_led):
        """determine back LED position (e.g back_left_led and back_right_led)
        """
        midpoint = self._midpoint(led1, led2)
        if led1['X'] <= led2['X']:
            if midpoint['Y'] >= front_led['Y']:
                #point 1 is left and point 2 is right
                self.back_left_led = led1
                self.back_right_led = led2
            else:
                # point 2 is left and point 1 is right
                self.back_left_led = led2
                self.back_right_led = led1
        else:
            if midpoint['Y'] >= front_led['Y']:
                # point 2 is left and point 1 is right
                self.back_left_led = led2
                self.back_right_led = led1
            else:
                # point 1 is left and point 2 is right
                self.back_left_led = led1
                self.back_right_led = led2
