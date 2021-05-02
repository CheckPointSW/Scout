from scout.scout_api import *

##############################
## Extended API Error Codes ##
##############################

embedded_error_codes = {  # Example for a project-specific error code
                         30: "STATUS_INVALID_FREE",
                       }

addErrorCodes(embedded_error_codes)

#############################
## Camera API Instructions ##
#############################

EMBEDDED_INST_BASIC_INSTR = SCOUT_MAX_BASIC_INSTR + 1
EMBEDDED_INST_ALLOC       = EMBEDDED_INST_BASIC_INSTR + 0
EMBEDDED_INST_FREE        = EMBEDDED_INST_BASIC_INSTR + 1

#########################
## Instruction Factory ##
#########################

def instrAlloc(size):
    """Allocates a memory buffer on the target

    Args:
        size (int): size (in bytes) of the desired memory allocation

    Return Value:
        string containing the serialized instruction
    """
    return addHeader(EMBEDDED_INST_ALLOC, struct.pack("!L", size))

def instrFree(address):
    """Frees a memory allocation on the target, on the specified address

    Args:
        address (int): memory address of the desired memory allocation

    Return Value:
        string containing the serialized instruction
    """
    return addHeader(EMBEDDED_INST_FREE, struct.pack("!L", address))
