#!/usr/bin/python

from embedded_scout_api  import *
from scout.scout_network import *
from elementals          import Prompter, hexDump

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
    logger.info('Starting to manage the embedded Scout')

    logger.info('Allocating a remote memory buffer')
    data = sendInstr(sock_fd, instrAlloc(0x100), logger)

    memory_addr = struct.unpack('!L', data)[0]
    logger.info('The buffer was allocated at address: 0x%08x', memory_addr)

    logger.info('Sending the memory read instruction')
    data = sendInstr(sock_fd, instrMemRead(memory_addr, 0x100), logger)
    logger.info('The default content of the buffer is:')
    logger.addIndent()
    logger.info(hexDump(data))
    logger.removeIndent()

##
# Prints the usage instructions (example)
##
def printUsage(args):
    print(f'Usage: {args[0]} <server_ip>')
    print('Exiting')
    exit(1)

##
# Main function (example)
##
def main(args):
    # Check the arguments
    if len(args) != 1 + 1:
        print(f'Wrong amount of arguments, got {len(args) - 1}, expected 1')
        printUsage(args)

    # parse the args
    server_ip = args[1]

    # open the log
    prompter = Prompter('Scout Manager', [('scout_log.txt', 'a', logging.DEBUG)])

    # connect to the server
    sock_fd = socket.create_connection((server_ip, SCOUT_PORT))

    # configure the scout
    setBitness32()

    # start the managing session
    startManage(sock_fd, prompter)

    prompter.info('Finished Successfully')

if __name__ == '__main__':
    main(sys.argv)