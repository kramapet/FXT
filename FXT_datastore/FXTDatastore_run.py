#!/usr/bin/env python3

import sys
import os
from optparse import OptionParser
from rpyc.utils.classic import DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT
from rpyc.utils.server import ThreadedServer, ForkingServer
from rpyc.lib import setup_logger
from rpyc.core import SlaveService
import rpyc

from src.FXTDatastore import FXTDatastore

def setup_optparser():
    parser = OptionParser()
    
    ###########################################################################
    # RPYC server options
    ###########################################################################
    # MODE option
    parser.add_option("--mode", action="store", dest="mode", metavar="MODE",
        default="threaded", type="string", help="mode can be 'threaded', 'forking', "
        "or 'stdio' to operate over the standard IO pipes (for inetd, etc.). "
        "Default is 'threaded'")
    
    # TCP options
    parser.add_option("--port", action="store", dest="port", type="int",
        metavar="PORT", default=None,
        help="specify a different TCP listener port (default = %s, default for SSL = %s)" %
            (DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT))
    parser.add_option("--host", action="store", dest="host", type="str",
        metavar="HOST", default="", help="specify a different "
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

    ###########################################################################
    # Dataserver options
    ###########################################################################

    return parser

def process_parameters(parser, options):
    server_arguments = {'mode':options.mode.lower(), 'hostname':options.host, 'port':DEFAULT_SERVER_PORT,
                             'reuse_addr':True, 'ipv6':options.ipv6, 'authenticator':None, 'quiet':options.quiet}
    if options.ssl_keyfile or options.ssl_certfile or options.ssl_cafile:
        if not options.ssl_keyfile:
            parser.error("SSL: keyfile required")
        if not options.ssl_certfile:
            parser.error("SSL: certfile required")
            server_arguments['port'] = SSLAuthenticator(options.ssl_keyfile, options.ssl_certfile, options.ssl_cafile)
        if not options.port:
            server_arguments['port'] = DEFAULT_SERVER_SSL_PORT
    return server_arguments
    
def run(options, server_arguments):
    if server_arguments['mode'] == 'threaded':
        setup_logger(options)
        t = ThreadedServer(FXTDatastore, hostname = server_arguments['hostname'],
            port = server_arguments['port'], reuse_addr = server_arguments['reuse_addr'], ipv6 = server_arguments['ipv6'],
            authenticator = server_arguments['authenticator'])
        t.logger.quiet = server_arguments['quiet']
        t.start()
    elif server_arguments['mode'] == 'forking':
        setup_logger(options)
        t = ForkingServer(FXTDatastore, hostname = server_arguments['hostname'],
            port = server_arguments['port'], reuse_addr = server_arguments['reuse_addr'], ipv6 = server_arguments['ipv6'],
            authenticator = server_arguments['authenticator'])
        t.logger.quiet = server_arguments['quiet']
        t.start()
    elif server_arguments['mode'] == 'stdio':
        setup_logger(options)
        origstdin = sys.stdin
        origstdout = sys.stdout
        if server_arguments['quiet']:
            dev = os.devnull
        elif sys.platform == "win32":
            dev = "con:"
        else:
            dev = "/dev/tty"
        try:
            sys.stdin = open(dev, "r")
            sys.stdout = open(dev, "w")
        except (IOError, OSError):
            sys.stdin = open(os.devnull, "r")
            sys.stdout = open(os.devnull, "w")
        conn = rpyc.classic.connect_pipes(origstdin, origstdout)
        try:
            try:
                conn.serve_all()
            except KeyboardInterrupt:
                print("User interrupt!")
        finally:
            conn.close()
    else:
        print("Wrong mode!")


if __name__ == '__main__':
    parser = setup_optparser()
    options, args = parser.parse_args()
    server_arguments = process_parameters(parser, options)
    run(options, server_arguments)
    
    
    