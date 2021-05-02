import struct

#############################
##  Static Configurations  ##
#############################

GOT_START_MARKER = struct.pack(">L", 0x11222211)
GOT_END_MARKER   = struct.pack(">L", 0x33444433)

# Variables (sizes only)
scout_instructions_globals_32_size = 4 + 10 * 16
scout_instructions_globals_64_size = 8 + 10 * 24
scout_static_buffers_32_size = 0x1006 + 2 + 0x1000
scout_static_buffers_64_size = 0x1006 + 2 + 0x1000

scout_got_base_size = 12
scout_got_base_size_mmap = scout_got_base_size + 3
# Scout GOT symbols order:
# * memcpy
# * memset
# * malloc
# * free
# * socket
# * bind
# * listen
# * accept
# * connect
# * recv
# * send
# * close
# If compiled using MMAP, we also have the following:
# * mmap
# * mprotect
# * munmap

def placeContext(got, globals, binary_file, logger):
    """Embedds the PIC context into the compiled binary blob

    Args:
        got (bytes): Content of the PIC GOT
        globals (bytes): Content of the PIC global variables
        binary_file (string): path to the PIC binary that will host the context
        logger (logger): (elementals) logger
    """
    # 1. Open the file (read)
    fd = open(binary_file, "rb")
    raw_binary = fd.read()
    fd.close()

    # 2. Locate the GOT
    got_start = raw_binary.find(GOT_START_MARKER)
    got_end   = raw_binary.find(GOT_END_MARKER) + len(GOT_END_MARKER)
    # Sanity check
    if got_start < 0 or got_end <= got_start:
        logger.error("Failed to locate the GOT markers in the PIC binary")
        return

    # 3. Size checking
    wanted_context = got + globals
    if got_end - got_start != len(wanted_context):
        logger.error("Mismatching context sizes, found 0x%x and generated 0x%x", got_end - got_start, len(wanted_context))
        return

    # 4. Update the value
    logger.info("Placing the generated context in it's place")
    pic_binary = raw_binary[:got_start] + wanted_context + raw_binary[got_end:]

    # 5. Open the file (write)
    fd = open(binary_file, "wb")
    fd.write(pic_binary)
    fd.close()

    logger.info(f"Complete PIC binary was saved to: {binary_file}")
