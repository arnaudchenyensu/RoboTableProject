import requests


class Network(object):
    """Create a Network object."""

    def get(self, addr, action=None):
        """Get data from other table.

        :param addr: Address of the table.
        :param action: Action name (e.g get_irs, is_ready...).

        Note: You need to override this method if you want to implement
        your own action.

        Usage::

            >>> n = Network()
            >>> n.get('10.4.9.11', 'get_irs')
            {'front': {'X': 10, 'Y': 20}, 'left': {'X': 103, 'Y': 23}, 'right': {'X': 111, 'Y': 203}}

        """
        if action == 'get_irs':
            addr += '/get_irs/'
        r = requests.get(addr)
        return r.text
