from nose.tools import *
from RoboTableProject.game import Game


class RobotTest(object):
    """Simple Robot class test"""
    def __init__(self):
        self.front_led = {'X': 100, 'Y': 300}
        self.left_led = {'X': 203, 'Y': 423}
        self.right_led = {'X': 609, 'Y': 567}
        self.leds = {'front': self.front_led, 'left': self.left_led, 'right': self.right_led}


class SensorTest(object):
    """Simple Sensor class test"""
    def __init__(self):
        self.height_resolution = 768


sensor = SensorTest()
game = Game('myGame', sensor, test=True)
game.sensor = sensor
x_factors = [0.06227100287030414, 0.0054334502504480965, 9.9951064607119537]
y_factors = [-0.01630035075134428, 0.18681300861091266, -10.145777867657028]
game.x_factors = x_factors
game.y_factors = y_factors
robot = RobotTest()
game.robot = robot


def test_calculate_calibration():
    leds_location_screen = [[64, 384], [192, 192], [192, 576]]
    leds_location_wiimote = [[678, 2169], [2807, 1327], [2629, 3367]]
    x_factors_test, y_factors_test = game.calculate_calibration(leds_location_screen, leds_location_wiimote)
    assert_equal(x_factors_test, x_factors)
    assert_equal(y_factors_test, y_factors)


def test_robot_leds_property():
    expected_front_led = {'X': 17.852241822876795, 'Y': 76.9917123588394}
    expected_left_led = {'X': 24.934469499323242, 'Y': 53.89826950447018}
    expected_right_led = {'X': 50.99891350073124, 'Y': 26.572336685137028}
    expected_leds = {'front': expected_front_led, 'left': expected_left_led, 'right': expected_right_led}
    leds_test = game.robot_leds
    assert_equal(expected_leds, leds_test)
