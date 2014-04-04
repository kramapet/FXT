#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rpyc
from rpyc.utils.classic import DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT
from optparse import OptionParser

class FXTMaster():
    def __init__(self):
        parser = self._setup_optparser()
        options, args = parser.parse_args()
        self.client_arguments = self._process_parameters(parser, options)
        
        self.datastore = None

    def _setup_optparser(self):
        parser = OptionParser()
        
        ###########################################################################
        # Master options
        ###########################################################################
        # TCP options
        parser.add_option("--port", action="store", dest="port", type="int",
            metavar="PORT", default=None,
            help="specify a different TCP listener port (default = %s, default for SSL = %s)" %
                (DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT))
        parser.add_option("--host", action="store", dest="host", type="str",
            metavar="HOST", default="localhost", help="specify a different "
            "host to bind to. Default is INADDR_ANY")
        parser.add_option("--ipv6", action="store_true", dest="ipv6",
            metavar="HOST", default=False, help="whether to enable ipv6 or not. " 
            "Default is false")
    
        # logging
        parser.add_option("--logfile", action="store", dest="logfile", type="str",
            metavar="FILE", default=None, help="specify the log file to use; the "
            "default is stderr")
        parser.add_option("--quiet", action="store_true", dest="quiet",
            default=False,
            help="quiet mode (no logging). in stdio mode, writes to /dev/null")
        
        # SSL
        parser.add_option("--ssl-keyfile", action="store", dest="ssl_keyfile", metavar="FILENAME",
            default=None, help="the keyfile to use for SSL. required for SSL")
        parser.add_option("--ssl-certfile", action="store", dest="ssl_certfile", metavar="FILENAME",
            default=None, help="the certificate file to use for SSL. required for SSL")
        parser.add_option("--ssl-cafile", action="store", dest="ssl_cafile", metavar="FILENAME",
            default=None, help="the certificate authority chain file to use for SSL. "
            "optional, allows client-side authentication")
    
        # Run options
        parser.add_option("--test", action="store_true", dest="test",
            default=False, help="Run tests on data.")
        parser.add_option("--train", action="store_true", dest="train",
            default=False, help="Train model.")
        parser.add_option("--run", action="store_true", dest="run",
            default=False, help="Run trading.")
        return parser

    def _process_parameters(self, parser, options):
        client_arguments = {'hostname':options.host, 'port':DEFAULT_SERVER_PORT, 'authenticator':None, 'quiet':options.quiet}
        if options.ssl_keyfile or options.ssl_certfile or options.ssl_cafile:
            if not options.ssl_keyfile:
                parser.error("SSL: keyfile required")
            if not options.ssl_certfile:
                parser.error("SSL: certfile required")
                client_arguments['port'] = SSLAuthenticator(options.ssl_keyfile, options.ssl_certfile, options.ssl_cafile)
            if not options.port:
                client_arguments['port'] = DEFAULT_SERVER_SSL_PORT
        return client_arguments
        
    def _connect_to_datastore(self, host, port):
        print("connecting to ", host, ":", port)
        self.datastore_conn = rpyc.connect(host, port)
    
    def _get_data_ranges(self, symbol=None):
        print(self.datastore_conn.root.exposed_get_data_ranges(symbol))
    
    def _get_data(self):
        pass

    def run(self):
        self._connect_to_datastore(self.client_arguments['hostname'], self.client_arguments['port'])
        self._get_data_ranges('EUR/USD')

    def run_test(self):
        pass
    
    def run_real(self):
        pass

if __name__ == '__main__':
    master = FXTMaster()
    master.run()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4   