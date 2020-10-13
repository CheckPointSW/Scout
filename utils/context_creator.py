#!/usr/bin/python

import os
import sys
import time
import struct

#############################
##  Static Configurations  ##
#############################

GOT_START_MARKER    = struct.pack(">L", 0x11222211)
GOT_END_MARKER      = struct.pack(">L", 0x33444433)

# Variables (sizes only)
scout_instructions_globals_32_size = 4 + 10 * 16
scout_instructions_globals_64_size = 8 + 10 * 24
scout_static_buffers_32_size = 0x1006 + 2 + 0x1000
scout_static_buffers_64_size = 0x1006 + 2 + 0x1000

########################
##  Global Variables  ##
########################

globals_size = None
full_got     = None

def generateGOT(symbol_memcpy, symbol_memset, symbol_malloc, symbol_free, symbol_socket, symbol_bind,
                symbol_listen, symbol_accept, symbol_connect, symbol_recv, symbol_send, symbol_close,
		        symbol_mmap=None, symbol_mprotect=None, symbol_munmap=None, project_got=[], is_thumb=False):
    """Generates the Global Offset Table (GOT) content using the supplied addresses

    Args:
        symbol_memcpy (int): (virtual) address of the memcpy() function in the hosting address space
        symbol_memset (int): (virtual) address of the memset() function in the hosting address space
        symbol_malloc (int): (virtual) address of the malloc() function in the hosting address space
        symbol_free (int): (virtual) address of the free() function in the hosting address space
        symbol_socket (int): (virtual) address of the socket() function in the hosting address space
        symbol_bind (int): (virtual) address of the bind() function in the hosting address space
        symbol_listen (int): (virtual) address of the listen() function in the hosting address space
        symbol_accept (int): (virtual) address of the accept() function in the hosting address space
        symbol_connect (int): (virtual) address of the connect() function in the hosting address space
        symbol_recv (int): (virtual) address of the send() function in the hosting address space
        symbol_close (int): (virtual) address of the close() function in the hosting address space
        symbol_mmap (int, optional): (virtual) address of the mmap() function, or None if unused (None by default)
        symbol_mprotect (int, optional): (virtual) address of the mprotect() function, or None if unused (None by default)
        symbol_munmap (int, optional): (virtual) address of the munmap() function, or None if unused (None by default)
        project_got (list): list of additional memory addresses for symbols used in the project's GOT
        is_thumb (bool): True iff the scout was compiled to be executed inside an ARM thumb binary
    """
    global full_got

    full_got  = [ symbol_memcpy, symbol_memset, symbol_malloc, symbol_free,
                  symbol_socket, symbol_bind, symbol_listen, symbol_accept, symbol_connect, symbol_recv, symbol_send, symbol_close,
                ]
    if symbol_mmap is not None:
        full_got += [symbol_mmap, symbol_mprotect, symbol_munmap]

    full_got += project_got

    # Check if we need to adjust it
    if is_thumb:
        full_got = [x + 1 for x in full_got]

def generateGlobals(scout_vars_size=scout_instructions_globals_32_size, project_vars_size=0):
    """Configures the globals blob using the supplied sizes

    Args:
        scout_vars_size (numeric): size in bytes of the base scout's globals (scout_instructions_globals_32_size by default)
        project_vars_size (numeric): size in bytes of the project's scout globals (0 by default)
    """
    global globals_size

    globals_size = scout_vars_size + project_vars_size

def createContext(is_little_endian, is_32_bit):
    """Creates the PIC context matching the target's architecture

    Args:
        is_little_endian (bool): True iff the scout was compiled to little endian
        is_32_bit (bool): True iff the scout was compiled to 32 bits
    """
    got = b''
    # functions
    for func in full_got:
        got += struct.pack(("<" if is_little_endian else ">") + ("L" if is_32_bit else "Q"), func)
    # globals
    got += b'\x00' * globals_size
    # functions
    return got

def placeContext(compiled_file, shellcode_file, is_little_endian, is_32_bit, logger):
    """Embedds the PIC context into the compiled binary blob

    Args:
        compiled_file (string): path to the compiled PIC binary (NOT the ELF)
        shellcode_file (string): path to the (created) full PIC shellcode
        is_little_endian (bool): True iff the scout was compiled to little endian
        is_32_bit (bool): True iff the scout was compiled to 32 bits
        logger (logger): (elementals) logger
    """
    # 0. Sanity checks
    if globals_size is None:
        logger.error("Undefined size for the global variables...")
        return

    if full_got is None:
        logger.error("Undefined function addresses for the GOT...")
        return

    # 1. Open the file (read)
    fd = open(compiled_file, "rb")
    raw_shellcode = fd.read()
    fd.close()

    # 2. Locate the GOT
    got_start = raw_shellcode.find(GOT_START_MARKER)
    got_end   = raw_shellcode.find(GOT_END_MARKER) + len(GOT_END_MARKER)
    # Sanity check
    if got_start < 0 or got_end <= got_start:
        logger.error("Failed to locate the GOT markers in the shellcode")
        return

    # 3. Generate the needed values
    logger.info("Generating the context values")
    wanted_context = createContext(is_little_endian, is_32_bit)

    # 4. Size checking
    if got_end - got_start != len(wanted_context):
        logger.error("Mismatching context sizes, found 0x%x and generated 0x%x", got_end - got_start, len(wanted_context))
        return

    # 5. Update the value
    logger.info("Placing the generated context in it's place")
    shellcode = raw_shellcode[:got_start] + wanted_context + raw_shellcode[got_end:]

    # 6. Open the file (write)
    fd = open(shellcode_file, "wb")
    fd.write(shellcode)
    fd.close()

    logger.info(f"Complete shellcode was saved to: {shellcode_file}")
