from django.http import HttpResponse
import cwiid
import time
from django.utils import simplejson
from django.shortcuts import render_to_response
from RoboTableProject.game import Game
from RoboTableProject.wiimote import Wiimote
from RoboTableProject.network import Network
import Queue
import threading

# p = Process(target=_bulk_action,args=(action,objs))
# p.start()
# return HttpResponse()

# def hello(request):
#     # execfile("../wii_remote_1.py")
#     test()
#     print "Chargement de la page"
#     return HttpResponse('OK')


g = None
t = None


def start_game(request):
    # wiimote = Wiimote()
    # g = Game('test', wiimote)
    # path_img = '../temp5.jpg'
    # g.load_map(path_img)

    # # Thread
    # t = threading.Thread(target=g.start)
    # t.daemon = True
    # t.start()
    # t.run()

    # Process
    # p = Process(target=g.start)
    # p.start()
    # p.run()

    t = threading.Thread(target=launch)
    # Daemon thread stop when the program exits
    t.daemon = True
    t.start()

    # t.join()
    # g.start()
    # execfile("main.py")
    return HttpResponse('Game started')


def launch():
    global g
    print 'Launch function...'
    time.sleep(5)

    wiimote = Wiimote()
    network = Network()
    servers = ['http://10.4.9.1:8001/', 'http://10.4.9.1:8002/']
    g = Game(wiimote, network, servers=servers)
    path_img = '../temp5.jpg'
    g.load_map(path_img)
    g.start()
    # t = threading.Thread(target=g.start)
    # t.daemon = True
    # t.start()
    # t.run()


def stop_game(request):
    g.stop()
    return HttpResponse('Game stopped')

# def connect(request):
#     print 'Press 1 + 2 on your Wii Remote now ...'
#     time.sleep(1)

#     # Connect to the Wii Remote. If it times out
#     # then quit.
#     try:
#         global wii
#         wii = cwiid.Wiimote()
#         wii.led = 1
#         return HttpResponse("Connection established")
#     except RuntimeError:
#         return HttpResponse("Error opening wiimote connection")
#         quit()


# def disconnect(request):
#     global wii
#     wii.rumble = 1
#     time.sleep(1)
#     wii.rumble = 0
#     wii = 0
#     return HttpResponse("Connection closed")


def irs():
    global wii
    wii.rpt_mode = cwiid.RPT_IR
    irs = []
    for src in wii.state['ir_src']:
        if src:
            pos = {
                "X": src['pos'][0],
                "Y": src['pos'][1]
            }
            irs.append(pos)
        else:
            pos = {
                "X": -1,
                "Y": -1
            }
            irs.append(pos)
    return irs


def get_irs(request):
    global g
    # return HttpResponse(simplejson.dumps(irs()), mimetype='application/json')
    return HttpResponse(simplejson.dumps(g.robot_leds), mimetype='application/json')


def get_ir(request, ir_id):
    return HttpResponse(simplejson.dumps(irs()[int(ir_id)]), mimetype='application/json')


def index(request):
    return render_to_response('index.html')
