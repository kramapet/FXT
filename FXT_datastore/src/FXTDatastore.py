#!/usr/bin/env python3
"""
rpyc - service tutorial
    https://github.com/tomerfiliba/rpyc/blob/master/docs/tutorial/tut3.rst
"""

import rpyc

class FXTDatastore(rpyc.Service):
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_test_method(self): # this is an exposed method
        return 42

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"

    