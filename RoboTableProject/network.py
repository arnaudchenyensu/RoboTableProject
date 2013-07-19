import requests


class Network(object):
    """Create a Network object."""

    def __init__(self, addr=None):
        self.addr = addr

    def get(self, action=None, addr=None):
        """Get data from other table.

        :param action: Action name (e.g get_irs, is_ready...).

        Note: You need to override this method if you want to implement
        your own action.

        Usage::

            >>> n = Network()
            >>> n.get('10.4.9.11', 'get_irs')
            {'front': {'X': 10, 'Y': 20}, 'left': {'X': 103, 'Y': 23}, 'right': {'X': 111, 'Y': 203}}

        """
        if addr is None:
            addr = self.addr

        if action == 'get_irs':
            addr += '/irs/'
        r = requests.get(addr)
        return r.json()

    def get_leds(self):
        """Return a list of the location of leds detected.

        (e.g [{'X': 10, 'Y': 20}, {'X': 103, 'Y': 23}, {'X': 111, 'Y': 203}, {'X': 121, 'Y': 13}])

        Note: If the location of a led is not detected, X and Y equal -1.

        """
        return self.get(action='get_irs')
