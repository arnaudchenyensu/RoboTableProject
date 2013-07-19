from flask import Flask
from flask import render_template
from flask import json
# import cwiid
import time
from game import Game
from wiimote import Wiimote
from network import Network
import threading
app = Flask(__name__)
app.debug = True

g = None
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
    global g
    print 'Launch function...'
    time.sleep(5)

    wiimote = Wiimote()
    network = Network()
    servers = ['http://10.4.12.6:5000', 'http://10.4.12.6:5000']
    g = Game(wiimote, network, servers=servers)
    path_img = 'img/temp5.jpg'
    g.load_map(path_img)
    g.start()


@app.route("/stop_game/")
def stop_game():
    g.stop()
    return 'Game stopped'


@app.route("/irs/")
def irs():
    global g
    # return HttpResponse(simplejson.dumps(irs()), mimetype='application/json')
    # return HttpResponse(simplejson.dumps(g.robot_leds), mimetype='application/json')
    return json.dumps(g.robot_leds)

app.run(host='0.0.0.0')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
