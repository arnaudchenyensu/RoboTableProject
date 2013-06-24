from nose.tools import *
from RoboTableProject.game.game import Game

sensor = object()
game = Game('myGame', sensor, test=True)


def test_calculate_calibration():
    leds_location_screen = [[64, 384], [192, 192], [192, 576]]
    leds_location_wiimote = [[678, 2169], [2807, 1327], [2629, 3367]]
    x_factors = [0.06227100287030414, 0.0054334502504480965, 9.9951064607119537]
    y_factors = [-0.01630035075134428, 0.18681300861091266, -10.145777867657028]
    x_factors_test, y_factors_test = game.calculate_calibration(leds_location_screen, leds_location_wiimote)
    assert_equal(x_factors_test, x_factors)
    assert_equal(y_factors_test, y_factors)
