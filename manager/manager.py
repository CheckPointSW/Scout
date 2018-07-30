#!/usr/bin/python

from kernel_scout_api  import *
from scout_network     import *
from elementals        import Prompter

import logging
import struct
import time
import socket
import os
import sys

##
# Main debugging session (example)
##
def startManage(sock_fd, logger):
    logger.info('Starting to manage the proxy')

    logger.info('Sending the Leak instruction')
    data = sendInstr(sock_fd, instrLeakAddr(), logger)

    leaked_addr = struct.unpack("<Q", data)[0]
    logger.info("The leaked kernel address is: %016x" % (leaked_addr))

    logger.info('Sending the memory read instruction')
    data = sendInstr(sock_fd, instrMemRead((leaked_addr - 0x1000) & (2 ** 64 - 1 - (0x1000 - 1)), 256), logger)
    logger.info("The leaked data is: %s" % (data))
    logger.info("The leaked hex data is: %s" % (data.encode("hex")))

##
# Prints the usage instructions (example)
##
def printUsage(args):
    print 'Usage: %s <server_ip>' % (args[0])
    print 'Exitting'
    exit( 1 )

##
# Main function (example)
##
def main(args):
    # Check the arguments
    if len(args) != 1 + 1:
        print 'Wrong amount of arguments, got %d, expected %d' % (len(args) - 1, 1)
        printUsage( args )
        
    # parse the args
    server_ip = args[1]

    # open the log
    prompter = Prompter("Scout Manager", [("proxy_log.txt", "a", logging.DEBUG)])

    # connect to the server
    sock_fd = socket.create_connection((server_ip, SCOUT_PORT))

    # configure the scout
    setBitness64()
    
    # start the managing session
    startManage(sock_fd, prompter)

    prompter.info('Finished Successfully')

if __name__ == "__main__":
    main(sys.argv)
