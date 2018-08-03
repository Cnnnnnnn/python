import httplib
import urllib
import time
import json


class Transaction(object):
    def __init__(self):
        self.customer_timers = {}

    def run(self):
        conn = httplib.Httpconnection("localhost:8080")
        headers = {"connect-type": "application/json"}
        params =
        start = time.time()
