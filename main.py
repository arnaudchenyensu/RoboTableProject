from RoboTableProject.game import Game
from RoboTableProject.game import GameManagement
from RoboTableProject.wiimote import Wiimote
from RoboTableProject.robot import Robot
from RoboTableProject.network import Network
from RoboTableProject.graphic import GUI

# This file is only use to make test on the Robot Table
wiimote = Wiimote()
network = Network()
gui = GUI()
game_management = GameManagement(wiimote, gui, network, 2)
servers = ['http://10.4.9.4:5000', 'http://10.4.9.1:5000']
robot = Robot(wiimote, gui=gui)
robot2 = Robot(network)
remote_server_object = Game(robot2, remote=True)


g = Game(robot, gui=gui, game_management=game_management, remote_server_object=remote_server_object,
         main_server=True, addr_remote_servers=servers)
path_img = 'RoboTableProject/img/temp5.jpg'
g.load_map(path_img)
g.start()
