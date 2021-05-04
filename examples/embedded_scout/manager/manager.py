#!/usr/bin/python3

from embedded_scout_api           import *
from scout_debugger.scout_network import *
from elementals                   import Prompter, hexDump

import logging
import struct
import socket
import time
import sys

##
# Main debugging session (example)
##
def startManage(sock_fd, logger):
    logger.info('Starting to manage the embedded Scout')

    logger.info('Allocating a remote memory buffer')
    data = sendInstr(sock_fd, instrAlloc(0x100), logger)

    memory_addr = struct.unpack("<L" if isBitness32() else "<Q", data)[0]
    logger.info('The buffer was allocated at address: 0x%012x', memory_addr)

    logger.info('Reading from the just allocated memory')
    data = sendInstr(sock_fd, instrMemRead(memory_addr, 0x100), logger)
    logger.info('The default content of the buffer is:')
    logger.addIndent()
    logger.info(hexDump(data))
    logger.removeIndent()

    logger.info("Writing to the allocated memory")
    sendInstr(sock_fd, instrMemWrite(memory_addr + 0x70, b"Scout was here!"), logger)

    logger.info('Reading again from the same memory address')
    data = sendInstr(sock_fd, instrMemRead(memory_addr, 0x100), logger)
    logger.info('The updated content of the buffer is:')
    logger.addIndent()
    logger.info(hexDump(data))
    logger.removeIndent()

##
# Prints the usage instructions (example)
##
def printUsage(args):
    print(f'Usage: {args[0]} <server_ip> [full_scout.bin]')
    print('Exiting')
    exit(1)

##
# Main function (example)
##
def main(args):
    # Check the arguments
    if len(args) not in [1 + 1, 1 + 2]:
        print(f'Wrong amount of arguments, got {len(args) - 1}, expected 1/2')
        printUsage(args)

    # parse the args
    server_ip  = args[1]

    # open the log
    prompter = Prompter('Scout Manager', [('scout_log.txt', 'a', logging.DEBUG)])

    # Check if we need to load the full scout before connecting to it
    if len(args) == 1 + 2:
        scout_path = args[2]
        full_scout = open(scout_path, "rb").read()
        remoteLoadServer(server_ip, full_scout, prompter)
        prompter.info("Waiting for Scout to fully load")
        time.sleep(2)

    # connect to the server
    prompter.info("Connecting to the fully loaded scout")
    sock_fd = socket.create_connection((server_ip, SCOUT_PORT))

    # configure the scout
    setBitness32()

    # start the managing session
    startManage(sock_fd, prompter)

    prompter.info('Finished Successfully')


if __name__ == '__main__':
    main(sys.argv)
