from RoboTableProject.game.game import Game
from RoboTableProject.tracking.wiimote import Wiimote
from RoboTableProject.robot.robot import Robot


# This file is only use to make test on the Robot Table
wiimote = Wiimote()
g = Game('test')
path_img = '../../temp5.jpg'
g.load_map(path_img)
g.start()
