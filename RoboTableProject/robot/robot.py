import math


class Robot(object):
    """This class represent a Robot with 3 leds
        (2 at the back and 1 at the front)
    """

    def __init__(self, sensor):
        self.sensor = sensor
        self._front_led = {}
        self._back_left_led = {}
        self._back_right_led = {}

    @property
    def leds(self):
        """When this property is called, leds position is automatically updated
            and returned.
            (e.g {'front': {'X': 10, 'Y': 20},
                  'left': {'X': 103, 'Y': 23},
                  'right': {'X': 111, 'Y': 203},
                 }
            )
            Note: Since leds position is automatically updated at every call, you should save
            leds location in a variable (e.g leds = robot.leds)
        """
        leds_location = self.sensor.get_leds()
        self._determine_led_position(leds_location[0], leds_location[1], leds_location[2])
        return {'front': self._front_led, 'left': self._back_left_led, 'right': self._back_right_led}

    @property
    def centre(self):
        leds = self.leds
        centreX = ((leds['left']['X'] + leds['right']['X']) / 2. + leds['front']['X']) / 2.
        centreY = ((leds['left']['Y'] + leds['right']['Y']) / 2. + leds['front']['Y']) / 2.
        return [centreX, centreY]

    def _determine_led_position(self, led1, led2, led3):
        """determine and set led position (e.g front_led, back_left_led and back_right_led)
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
        """determine and set back led position (e.g back_left_led and back_right_led)
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

    def find_orientation(self, centreX, centreY, front_led_X, front_led_Y):
        orientation = 0

        direction = self._find_direction(centreX, centreY, front_led_X, front_led_Y)
        tan = (front_led_Y - centreY) / (front_led_X - centreX)
        if (tan < 0):
            tan = tan * -1.
        #because the robotable is flipped, the final oreintation will add 90 circuit degree.
        if direction == "UR":
            orientation = math.degrees(math.atan(tan))
        elif direction == "UL":
            orientation = 180 - math.degrees(math.atan(tan))
        elif direction == "DL":
            orientation = 180 + math.degrees(math.atan(tan))
        elif direction == "DR":
            orientation = 360 - math.degrees(math.atan(tan))
        elif direction == "R":
            orientation = 0
        elif direction == "U":
            orientation = 90
        elif direction == "L":
            orientation = 180
        elif direction == "D":
            orientation = 360
        elif direction == "N":
            orientation = 0

        return orientation

    def _find_direction(self, point1_x, point1_y, point2_x, point2_y):
        Y_dist = point2_y - point1_y
        X_dist = point2_x - point1_x

        if Y_dist > 0 and X_dist > 0:
            #Uper Right but it is UL on the screen
            return "UR"
        if Y_dist > 0 and X_dist < 0:
            #Uper Left but it is UR on the screen
            return "UL"
        if Y_dist < 0 and X_dist < 0:
            #Down Left but it is DR on the screen
            return "DL"
        if Y_dist < 0 and X_dist > 0:
            #Down Right but it is DL on the screen
            return "DR"
        if Y_dist == 0 and X_dist > 0:
            #Right
            return "R"
        if Y_dist > 0 and X_dist == 0:
            #Uper
            return "U"
        if Y_dist == 0 and X_dist < 0:
            #Left
            return "L"
        if Y_dist < 0 and X_dist == 0:
            #Down
            return "D"
        #default: not change at all
        return "N"
