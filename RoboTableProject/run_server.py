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
    addr_main_server = '10.4.9.4'
    robot = Robot(wiimote, gui=gui)

    game = Game(robot, wiimote, network, gui, game_management, addr_main_server)
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
    return json.dumps(game.robot.leds)


@app.route("/ready/")
def is_ready():
    global game_management
    return json.dumps(game_management.ready)


@app.route("/servers_ready/", methods=['GET', 'POST'])
def servers_ready():
    global game_management
    if request.method == 'POST':
        game_management.servers_ready = True
    return json.dumps(game_management.servers_ready)

@app.route("/servers/", methods=['GET', 'POST'])
def servers():
    global game_management
    if request.method == 'POST':
        game_management.servers = json.loads(request.get_data())
    return json.dumps(game_management.servers)

@app.route("/servers/new/", methods=['POST'])
def new_server():
    global game_management
    game_management.servers.append(json.loads(request.get_data()))
    return json.dumps(True)

@app.route("/launch/", methods=['POST'])
def launch_game():
    global game_management
    game_management.servers_ready = True
    return json.dumps(True)

app.run(host='0.0.0.0')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
