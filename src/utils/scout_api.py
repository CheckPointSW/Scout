import struct

####################
## Configurations ##
####################

TARGET_BITNESS = 32

###########################
## Basic API Error Codes ##
###########################

error_codes = {     # General errors
                     0: "STATUS_OK",
                     1: "STATUS_FAILURE",
                     2: "STATUS_INVALID_ARGS",
                     3: "STATUS_ALLOC_FAILED",
                     4: "STATUS_TCP_SOCK_FAILED",
                     5: "STATUS_TCP_BIND_FAILED",
                     6: "STATUS_TCP_LISTEN_FAILED",
                     7: "STATUS_TCP_ACCEPT_FAILED",
                     8: "STATUS_TCP_CONNECT_FAILED",
                     9: "STATUS_TCP_RECV_FAILED",
                    10: "STATUS_TCP_SEND_FAILED",

                    # Scout API
                    20: "STATUS_SMALL_HEADER",
                    21: "STATUS_ILLEGAL_LENGTH",
                    22: "STATUS_ILLEGAL_INSTR_ID"
              }

############################
## Basic API Instructions ##
############################

SCOUT_INST_NOP          = 0
SCOUT_INST_MEM_READ     = 1
SCOUT_INST_MEM_WRITE    = 2

SCOUT_MAX_BASIC_INSTR   = SCOUT_INST_MEM_WRITE

##############################
## Network API Instructions ##
##############################

LOADER_PORT = 0x2561
SCOUT_PORT  = 0x2562

#######################
## Configuration API ##
#######################

def setBitness32():
    """Set the module's bitness to match a 32 bit server."""
    global TARGET_BITNESS

    TARGET_BITNESS = 32

def setBitness64():
    """Set the module's bitness to match a 64 bit server."""
    global TARGET_BITNESS

    TARGET_BITNESS = 64

def isBitness32():
    """Check if the given bitness configuration is for 32-bits."""
    return TARGET_BITNESS == 32

def addErrorCodes(errors):
    """Add the given error codes to the supported dictionary.

    Args:
        errors (dict): new supported error codes in the form: <error ID> : <error string>
    """
    global error_codes

    for k, v in errors.items():
        error_codes[k] = v

#########################
## Instruction Factory ##
#########################

def addHeader(opcode, raw_instr):
    """Add the protocol's header to the given instruction.

    Args:
        opcode (int): instruction opcode ID
        raw_instr (string): binary data of the wanted instruction

    Return Value:
        string containing the complete serialized instruction
    """
    return struct.pack("!HL", opcode, len(raw_instr)) + raw_instr

# basic instructions
def instrNop():
    """Build the NOP (Ping) instruction.

    Args:
        (none)

    Return Value:
        string containing the serialized instruction
    """
    return addHeader(SCOUT_INST_NOP, b'')

def instrMemRead(addr, length):
    """Build the Read (Virtual) Memory instruction.

    Args:
        addr (int): (virtual) memory address
        length (int): number of bytes to be read form the given address

    Return Value:
        string containing the serialized instruction
    """
    instr = struct.pack("!QL" if TARGET_BITNESS == 64 else "!LL", addr, length)
    return addHeader(SCOUT_INST_MEM_READ, instr)

def instrMemWrite(addr, content):
    """Build the Write (Virtual) Memory instruction.

    Args:
        addr (int): (virtual) memory address
        content (string): binary data to be written to the given address

    Return Value:
        string containing the serialized instruction
    """
    instr = struct.pack("!Q" if TARGET_BITNESS == 64 else "!L", addr) + content
    return addHeader(SCOUT_INST_MEM_WRITE, instr)
