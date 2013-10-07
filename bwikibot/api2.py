
import requests
import json
from pprint import pprint

from bwikibot.path import config

class Wiki(object):
    def __init__(self, endpoint=None, throttle=1):
        ''' Create wiki client for given endpoint addres.  '''
        self._tokens = {}
        self.endpoint = endpoint
        self.throttle = throttle

        self.session = requests.Session()

        if endpoint:
            self.get_namespaces()
