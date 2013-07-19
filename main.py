from RoboTableProject.game import Game
from RoboTableProject.wiimote import Wiimote
from RoboTableProject.robot import Robot
from RoboTableProject.robot import RobotDrawing
from RoboTableProject.network import Network
import copy

# This file is only use to make test on the Robot Table
wiimote = Wiimote()
network = Network()
servers = ['http://10.4.9.1:5000', 'http://10.4.9.1:5000']
robot = Robot(wiimote, robot_drawing=RobotDrawing(None))
robot2 = copy.deepcopy(robot)
robot2.sensor = network
remote_server_object = Game(robot2, remote=True)


g = Game(robot, remote_server_object=remote_server_object,
         main_server=True, addr_remote_servers=servers)
path_img = 'RoboTableProject/img/temp5.jpg'
g.load_map(path_img)
g.start()
