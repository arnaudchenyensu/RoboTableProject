from nose.tools import *
from RoboTableProject.game.Game import Game


def test_game():
    game = Game('myGame')
    assert_equal(game.add(4, 5), 9)
