from nose.tools import *
from RoboTableProject.tracking.sensor_interface import SensorInterface
from RoboTableProject.robot.robot import Robot
import math


class SensorTest(SensorInterface):
    """Simple SensorTest class"""
    def get_leds(self):
        front_led = {"X": 3, "Y": 10}
        back_left = {"X": 5, "Y": 1}
        back_right = {"X": 2, "Y": 1}
        return [front_led, back_left, back_right]

# Resolution of the wiimote
width_resolution = 1024
height_resolution = 768

sensor = SensorTest(width_resolution, height_resolution)
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
    assert_equal(expected_centreX, robot.centreX)
    assert_equal(expected_centreY, robot.centreY)
