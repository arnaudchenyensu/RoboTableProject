from nose.tools import *
from RoboTableProject.robot.robotInterface import RobotInterface
import math


def test_robot():
    robot = RobotInterface()
    led1 = {"X": 7, "Y": 3}
    led2 = {"X": 1, "Y": 1}
    assert_equal(robot._distance_between_2_points(led1, led2), math.sqrt(40))
    assert_equal(robot._midpoint(led1, led2), {"X": 4, "Y": 2})
