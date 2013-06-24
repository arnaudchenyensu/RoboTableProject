from nose.tools import *
from RoboTableProject.game.game import Game


def test_game():
    leds_location_screen = [[64, 384], [192, 192], [192, 576]]
    leds_location_wiimote = [[678, 2169], [2807, 1327], [2629, 3367]]
    x_factors = [0.0623, 0.0054, 9.9951]
    y_factors = [-0.0163, 0.1868, -10.1458]
    game = Game('myGame')
    x_factors_test, y_factors_test = game.calculate_calibration(leds_location_screen, leds_location_wiimote)
    assert_equal(x_factors_test, x_factors)
    assert_equal(y_factors_test, y_factors)
