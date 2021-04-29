from scout.scout_api import *

##############################
## Extended API Error Codes ##
##############################

kernel_error_codes = { # Empty for now
                     }

addErrorCodes(kernel_error_codes)

#############################
## Kernel API Instructions ##
#############################

KERNEL_BASIC_INSTR      = SCOUT_MAX_BASIC_INSTR + 1
SCOUT_INST_PHY_READ     = KERNEL_BASIC_INSTR + 0
SCOUT_INST_PHY_WRITE    = KERNEL_BASIC_INSTR + 1
SCOUT_INST_LEAK_ADDR    = KERNEL_BASIC_INSTR + 2

#########################
## Instruction Factory ##
#########################

# kernel instructions
def instrPhyRead(addr, length):
    """Builds the Read Physical Memory instruction
    
    Args:
        addr (numeric): physical memory address
        length (numeric): number of bytes to be read form the given address

    Return Value:
        string containing the serialized instruction
    """
    instr = struct.pack( "!QL" if TARGET_BITNESS == 64 else "!LL", addr, length )
    return addHeader( SCOUT_INST_PHY_READ, instr )

def instrPhyWrite(addr, content):
    """Builds the Write Physical Memory instruction
    
    Args:
        addr (numeric): physical memory address
        content (string): binary data to be written to the given address

    Return Value:
        string containing the serialized instruction
    """
    instr = struct.pack( "!Q" if TARGET_BITNESS == 64 else "!L", addr ) + content
    return addHeader( SCOUT_INST_PHY_READ, instr )

def instrLeakAddr():
    """Builds the Leak Kernel Address instruction
    
    Args:
        (none)

    Return Value:
        string containing the serialized instruction
    """
    return addHeader( SCOUT_INST_LEAK_ADDR, b'' )