from flask import Flask
from flask import render_template
from flask import json
from flask import request
# import cwiid
import time
from game import Game
from game import GameManagement
from robot import Robot
from graphic import GUI
from wiimote import Wiimote
from network import Network
import threading

app = Flask(__name__)
app.debug = True

game = None
game_management = None
t = None


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)


@app.route("/start_game/")
def start_game():

    t = threading.Thread(target=launch)
    # Daemon thread stop when the program exits
    t.daemon = True
    t.start()

    return 'Game started'


def launch():
    global game
    global game_management
    print 'Launch function...'
    time.sleep(10)

    wiimote = Wiimote()
    network = Network()
    gui = GUI()
    game_management = GameManagement(wiimote, gui, network, 2)
    servers = ['http://10.4.9.4:5000', 'http://10.4.9.1:5000']
    robot = Robot(wiimote, gui=gui)
    robot2 = Robot(network)
    remote_server_object = Game(robot2, remote=True)


    game = Game(robot, gui=gui, game_management=game_management, remote_server_object=remote_server_object,
             main_server=True, addr_remote_servers=servers)
    path_img = 'RoboTableProject/img/temp5.jpg'
    game.load_map(path_img)
    game.start()


@app.route("/stop_game/")
def stop_game():
    game.stop()
    return 'Game stopped'


@app.route("/irs/")
def irs():
    global game
    return json.dumps(game.robot_leds)


@app.route("/is_ready/")
def is_ready():
    return json.dumps('True')


@app.route("/servers_ready/", methods=['GET', 'POST'])
def servers_ready():
    global game
    if request.method == 'POST':
        game.servers_ready = 'True'
    return json.dumps(game.servers_ready)

@app.route("/servers/", methods=['GET', 'POST'])
def servers():
    global game_management
    if request.method == 'POST':
        game_management.addr_servers.append(request.get_data())
        return json.dumps('True')
    return json.dumps(game_management.addr_servers)

@app.route("/launch/", methods=['POST'])
def launch():
    global game_management
    game_management.servers_ready = True
    return json.dumps('True')

app.run(host='0.0.0.0')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
