from game.game import Game
from tracking.sensor_interface import SensorInterface
from robot.robot import Robot


g = Game('test')
path_img = '../../temp5.jpg'
g.load_map(path_img)
g.start()
