from nose.tools import *
from RoboTableProject.tracking.sensor_interface import SensorInterface
from RoboTableProject.robot.robot import Robot
import math

robot = Robot(object())


def test_robot():
    led1 = {"X": 7, "Y": 3}
    led2 = {"X": 1, "Y": 1}
    assert_equal(robot._get_distance_between_2_points(led1, led2), math.sqrt(40))
    assert_equal(robot._get_midpoint(led1, led2), {"X": 4, "Y": 2})


def test_led_position():
    front_led = {"X": 3, "Y": 10}
    back_right = {"X": 2, "Y": 1}
    back_left = {"X": 5, "Y": 1}
    assert_equal(robot._determine_led_position(front_led, back_left, back_right), [front_led, back_left, back_right])
