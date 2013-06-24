from django.http import HttpResponse
import cwiid
import time
from django.utils import simplejson
from django.shortcuts import render_to_response

wii = 0

# def hello(request):
#     # execfile("../wii_remote_1.py")
#     test()
#     print "Chargement de la page"
#     return HttpResponse('OK')


def connect(request):
    print 'Press 1 + 2 on your Wii Remote now ...'
    time.sleep(1)

    # Connect to the Wii Remote. If it times out
    # then quit.
    try:
        global wii
        wii = cwiid.Wiimote()
        wii.led = 1
        return HttpResponse("Connection established")
    except RuntimeError:
        return HttpResponse("Error opening wiimote connection")
        quit()


def disconnect(request):
    global wii
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    wii = 0
    return HttpResponse("Connection closed")


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
    return HttpResponse(simplejson.dumps(irs()), mimetype='application/json')


def get_ir(request, ir_id):
    return HttpResponse(simplejson.dumps(irs()[int(ir_id)]), mimetype='application/json')

def index(request):
    return render_to_response('index.html')

