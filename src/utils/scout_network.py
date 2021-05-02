from scout_api import *
import struct
import socket

SCOUT_HEADER_FORMAT = "!LL"
SCOUT_HEADER_SIZE   = struct.Struct(SCOUT_HEADER_FORMAT).size

def sendInstr(sock, instr, logger):
    """Send an instruction to the (debuggee) server.

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
        logger.error(f"Failed to receive the header, got {len(header)} bytes")
        logger.removeIndent()
        return None

    status, size = struct.unpack(SCOUT_HEADER_FORMAT, header)
    if status not in error_codes:
        logger.error(f"Received invalid status: {status}")
        logger.removeIndent()
        return None
    if status != 0:
        logger.warning(f"Received status is: {error_codes[status]}")
    else:
        logger.debug("Status was OK")

    logger.debug(f"Output data size is: {size}")
    data = bytes()
    while size - len(data) > 0:
        data += sock.recv(size - len(data))
    logger.debug(f"Received {len(data)} output bytes")

    logger.removeIndent()
    return data

def remoteLoad(sock, full_scout):
    """Send the TCP loader the loading instruction for the full scout.

    Args:
        sock (socket): (TCP) socket to the remote loader
        full_scout (bin): binary (list of bytes) for the full scout
    """
    sock.send(struct.pack("!L", len(full_scout)) + full_scout)

def remoteLoadServer(ip, full_scout, logger, port=LOADER_PORT):
    """Connect to the remote TCP loader, and sends the full scout to be loaded.

    Args:
        ip (ip address): ip address of the remote scout loader
        full_scout (bin): binary (list of bytes) for the full scout
        logger (logger): (elementals) logger
        port (int, optional): TCP port for the remote loader (LODAER_PORT by default)
    """
    logger.info(f"Attempting to connect to the remote loader: {ip}:{port}")
    sock = socket.create_connection((ip, port))
    logger.info("Connected to the remote loader")
    remoteLoad(sock, full_scout)
    logger.info("Sent the loading instructions to the remote loader")
    sock.close()

def remoteLoadClient(ip, full_scout, logger, port=LOADER_PORT):
    """Create a local TCP server for which the remote loader could connect, and sends it the full scout.

    Args:
        ip (ip address): ip address for our server
        full_scout (bin): binary (list of bytes) for the full scout
        logger (logger): (elementals) logger
        port (int, optional): TCP port for the remote loader (LODAER_PORT by default)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind((ip, port))
    sock.listen(1)
    logger.info(f"Created the local TCP server: {ip}:{port}")

    loader_sock, loader_addr = sock.accept()
    logger.info(f"Accepted the remote loader from: {loader_addr[0]}")
    remoteLoad(loader_sock, full_scout)
    logger.info("Sent the loading instructions to the remote loader")
    sock.close()
