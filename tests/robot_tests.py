from nose.tools import *
from RoboTableProject.wiimote import Wiimote
from RoboTableProject.robot import Robot
import math


class SensorTest(Wiimote):
    """Simple SensorTest class"""

    def __init__(self):
        Wiimote.__init__(self, test=True)

    def get_leds(self):
        front_led = {"X": 3, "Y": 10}
        back_left = {"X": 5, "Y": 1}
        back_right = {"X": 2, "Y": 1}
        return [front_led, back_left, back_right]

sensor = SensorTest()
robot = Robot(sensor)


def test_robot():
    led1 = {"X": 7, "Y": 3}
    led2 = {"X": 1, "Y": 1}
    assert_equal(robot._get_distance_between_2_points(led1, led2), math.sqrt(40))
    assert_equal(robot._get_midpoint(led1, led2), {"X": 4, "Y": 2})


def test_led_position():
    leds = sensor.get_leds()
    expected_leds = {'front': leds[0], 'left': leds[1], 'right': leds[2]}
    obtained_leds = robot.leds
    assert_equal(obtained_leds, expected_leds)


def test_centre_property():
    expected_centreX = 3.25
    expected_centreY = 5.5
    centre = robot.centre
    centreX = centre[0]
    centreY = centre[1]
    assert_equal(expected_centreX, centreX)
    assert_equal(expected_centreY, centreY)
