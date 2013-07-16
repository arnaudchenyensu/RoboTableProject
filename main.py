from RoboTableProject.game import Game
from RoboTableProject.wiimote import Wiimote
from RoboTableProject.robot import Robot
from RoboTableProject.network import Network


# This file is only use to make test on the Robot Table
wiimote = Wiimote()
network = Network()
g = Game(wiimote, network)
path_img = '../temp5.jpg'
g.load_map(path_img)
g.start()
