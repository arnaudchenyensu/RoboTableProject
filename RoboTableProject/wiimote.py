import cwiid
import time


class Wiimote(object):
    """Create a Wiimote object and
    connect to the dongle USB.

    :param width_resolution: (optional) Width resolution of the sensor
    :param height_resolution: (optional) Height resolution of the sensor
    :param test: (optional) Only use for test-driven

    """
    def __init__(self, width_resolution=1024, height_resolution=768, test=False):
        self.width_resolution = width_resolution
        self.height_resolution = height_resolution
        self.wii = None
        if test is False:
            self.connect()

    def connect(self):
        """Connect the wiimote to the dongle Bluetooth."""
        print 'Press 1 + 2 on your Wii Remote now ...'
        time.sleep(2)

        # Connect to the Wii Remote. If it times out
        # then quit.
        try:
            self.wii = cwiid.Wiimote()
            self.wii.led = 1
            return True
        except RuntimeError:
            return False
            quit()

    def disconnect(self):
        """Disconnect the wiimote to the dongle Bluetooth."""
        self.wii.rumble = 1
        time.sleep(1)
        self.wii.rumble = 0
        self.wii = 0
        return 'Connection closed'

    def get_leds(self):
        """Return a list of the location of leds detected.

        (e.g [{'X': 10, 'Y': 20}, {'X': 103, 'Y': 23}, {'X': 111, 'Y': 203}, {'X': 121, 'Y': 13}])

        **Note:** If the location of a led is not detected, X and Y equal -1.

        """
        self.wii.rpt_mode = cwiid.RPT_IR
        irs = []
        for src in self.wii.state['ir_src']:
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
