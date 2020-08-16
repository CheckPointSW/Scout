#!/usr/bin/python
import os
import sys
import time
import struct
from elementals import Prompter

# Assuming the script is executed from its directory
sys.path.append('../../utils')

from scout_compiler  import *

##############################
##  Dynamic Configurations  ##
##############################

SCOUT_DIR           = '../../scout'

USER_SCOUT_BIN      = 'scout_user'

TARGET_ARCH         = ARC_INTEL
TARGET_ENDIANNESS   = True  # is little endian ?
TARGET_BITNESS      = False # is 32 bits ?

# project files list
project_files       = ['scout_user.c']

##
# Sets the bsaic architecture flags for our target
##
def setTargetFlags(logger):
    # 1. Set the architecture
    setScoutArc(TARGET_ARCH, is_32_bits=TARGET_BITNESS, is_little_endian=TARGET_ENDIANNESS, logger=logger)

    # 2. Set the environment
    setScoutEnv(is_pc=True)

    # 3. Set the permission mode
    setScoutMode(is_user=True)

##
# Compiles the user scout
##
def compileScout(logger):
    # 1. Set the target flags
    setTargetFlags(logger)

    # 2. Add additional flags:
    #  a) Will use the TCP server for instructions
    #  b) Will use dynamic buffers (malloc) for the received instructions
    #  c) Will act as a proxy scout, only passing on the instructions to the driver
    setScoutFlags([flag_instructions, flag_dynamic_buffers, flag_proxy])

    # 3. Define the working directories
    setWorkingDirs(project_dir='.', scout_dir = SCOUT_DIR)

    # 4. Generate the used compilation flags (we will rely on the defaults)
    compile_flags, link_flags=generateCompilationFlags(compile_flags=[], link_flags=[], logger=logger)

    # 5. Generate the list of compiled files
    compilation_files = [os.path.join(SCOUT_DIR, f) for f in scout_all_files] + project_files

    # 6. Compile the PC (user mode proxy) scout
    logger.info('Starting to compile the user scout')
    compilePCScout(compilation_files, compile_flags, link_flags, USER_SCOUT_BIN, logger)

    # Finished :)
    return

##
# Prints the usage instructions
##
def printUsage(args):
    print(f'Usage: {args[0].split(os.path.sep)[0]}')
    print('Exiting')
    exit(1)

##
# Main function
##
def main(args) :
    # Check the arguments (None for now)
    if len(args) != 1 + 0:
        print(f'Wrong amount of arguments, got {len(args) - 1}, expected 0')
        printUsage(args)

    # Create the logger
    prompter = Prompter()

    # Compile the user scout
    compileScout(prompter)

    prompter.info('Finished Successfully')

if __name__ == '__main__':
    main(sys.argv)
