from scout_api import *
import struct
import socket

SCOUT_HEADER_FORMAT = "!LL"
SCOUT_HEADER_SIZE   = struct.Struct(SCOUT_HEADER_FORMAT).size

def sendInstr(sock, instr, logger):
    """Sends an instruction to the (debuggee) server
    
    Args:
        sock (socket): (TCP) socket to the server
        instr (string): serialized instruction
        logger (logger): (elementals) logger

    Return Value:
        string containing the instruction's output, or None if error
    """
    logger.addIndent()

    sock.send(instr)
    # receive the header (stats, size)
    header = sock.recv(SCOUT_HEADER_SIZE)
    if len(header) != SCOUT_HEADER_SIZE:
        logger.error("Failed to receive the header, got %d bytes" % (len(header)))
        logger.removeIndent()
        return None

    status, size = struct.unpack(SCOUT_HEADER_FORMAT, header)
    if status not in error_codes:
        logger.error("Received invalid status: %d" % (status))
        logger.removeIndent()
        return None
    if status != 0:
        logger.warning("Received status is: %s" % (error_codes[status]))
    else :
        logger.debug("Status was OK")

    logger.debug("Output data size is: %d" % (size))
    data = ''
    while size - len(data) > 0:
        data += sock.recv(size - len(data))
    logger.debug("Received %d output bytes" % (len(data)))

    logger.removeIndent()
    return data
