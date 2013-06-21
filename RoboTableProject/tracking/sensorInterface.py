import cwiid
import time

wii = 0


class SensorInterface(object):
    """docstring for Tracking"""

    def __init__(self):
        self.connect()

    def connect(self):
        print 'Press 1 + 2 on your Wii Remote now ...'
        time.sleep(1)

        # Connect to the Wii Remote. If it times out
        # then quit.
        try:
            global wii
            wii = cwiid.Wiimote()
            wii.led = 1
            return True
        except RuntimeError:
            return False
            quit()

    def disconnect(self):
        global wii
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        wii = 0
        return 'Connection closed'

    def get_leds(self):
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
