import requests


class Network(object):
    """docstring for Network"""

    def get(self, addr, action=None):
        if action == 'get_irs':
            addr += '/get_irs/'
        r = requests.get(addr)
        return r.text
