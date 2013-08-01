import requests
import json


class Network(object):
    """Create a Network object."""

    def format(self, addr_server, port=5000):
        """Format the address and return it."""
        return 'http://' + addr_server + ':' + str(port)

    def get_irs(self, addr_server):
        """Return the IRs' location of a server."""
        addr_server = self.format(addr_server)
        addr_server += '/irs/'
        r = requests.get(addr_server)
        return r.json()

    def is_ready(self, addr_server):
        """Return True if the server is ready."""
        addr_server = self.format(addr_server)
        addr_server += '/ready/'
        r = requests.get(addr_server)
        return r.json()

    def launch(self, addr_server):
        """Launch the game on the server."""
        addr_server = self.format(addr_server)
        addr_server += '/launch/'
        r = requests.post(addr_server)
        return r.json()

    def send_addr(self, addr_server, addr_to_send):
        """Send an address to a server and return the response.

        :param addr_server: the address to send to.
        :param addr_to_send: the address to send.

        """
        addr_server = self.format(addr_server)
        addr_server += '/servers/new/'
        addr_to_send = json.dumps(addr_to_send)
        r = requests.post(addr_server, data=addr_to_send)
        return r.json()

    def send_list_servers(self, addr_server, list_servers):
        """Send a list of servers to a server."""
        addr_server = self.format(addr_server)
        addr_server += '/servers/'
        r = requests.post(addr_server, data=json.dumps(list_servers))
        return r.json()
