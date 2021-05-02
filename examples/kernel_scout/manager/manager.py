#!/usr/bin/python3

from kernel_scout_api             import *
from scout_debugger.scout_network import *
from elementals                   import Prompter, hexDump

import logging
import struct
import socket
import sys

##
# Main debugging session (example)
##
def startManage(sock_fd, logger):
    logger.info('Starting to manage the proxy')

    logger.info('Sending the Leak instruction')
    data = sendInstr(sock_fd, instrLeakAddr(), logger)

    v_leaked_addr, p_leaked_addr = struct.unpack('<QQ', data)
    logger.info('The leaked kernel virtual  address is: 0x%016x', v_leaked_addr)
    logger.info('The leaked kernel physical address is: 0x%016x', p_leaked_addr)

    logger.info('Sending the memory read instruction')
    data = sendInstr(sock_fd, instrPhyRead((p_leaked_addr - 0x1000) & (2 ** 64 - 1 - (0x1000 - 1)), 256), logger)
    if data:
        logger.info('The leaked data is:')
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
    prompter = Prompter('Scout Manager', [('proxy_log.txt', 'a', logging.DEBUG)])

    # connect to the server
    sock_fd = socket.create_connection((server_ip, SCOUT_PORT))

    # configure the scout
    setBitness64()

    # start the managing session
    startManage(sock_fd, prompter)

    prompter.info('Finished Successfully')


if __name__ == '__main__':
    main(sys.argv)
