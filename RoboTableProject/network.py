import requests
import json


class Network(object):
    """Create a Network object."""

    # def __init__(self, addr=None):
    #     self.addr = addr

    def get_irs(self, addr):
        addr += '/irs/'
        r = requests.get(addr)
        return r.json()

    def is_ready(self, addr):
        addr += '/ready/'
        r = requests.get(addr)
        return r.json()

    def launch(self, addr):
        addr += '/launch/'
        r = requests.post(addr)
        return r.json()

    def send_addr_servers(self, addr, addr_servers):
        pass
        # addr += '/servers/'
        # print 'Network.py:'
        # print addr
        # r = requests.post(addr, data=json.dumps(addr_servers))
        # return r.json()

    def send_list_servers(self, addr, list_servers):
        addr += '/servers/'
        r = requests.post(addr, data=json.dumps(list_servers))
        return r.json()

    # def get_leds(self):
    #     """Return a list of the location of leds detected.

    #     (e.g [{'X': 10, 'Y': 20}, {'X': 103, 'Y': 23}, {'X': 111, 'Y': 203}, {'X': 121, 'Y': 13}])

    #     **Note:** If the location of a led is not detected, X and Y equal -1.

    #     """
    #     return self.get(action='get_irs')
