#!/usr/bin/python
import os
import sys
from elementals import Prompter

from scout.scout_compiler import *

##############################
##  Dynamic Configurations  ##
##############################

SCOUT_DIR           = '../../../src/scout'

USER_SCOUT_BIN      = 'scout_user'

TARGET_ARCH         = ARC_INTEL

# project files list
project_files       = ['scout_user.c']

##
# Sets the bsaic architecture flags for our target
##
def setTargetFlags(logger):
    # 0. Create the compiler instance
    compiler = scoutCompiler(logger, is_pic=False)

    # 1. Set the architecture
    compiler.setArc(TARGET_ARCH)

    # 2. Set the permission mode (User & low CPU permissions, Kernel & High CPU permissions)
    compiler.setScoutMode(is_user=True)

    # 3. Set the working directories
    compiler.setWorkingDirs(project_dir='.', scout_dir=SCOUT_DIR)

    return compiler

##
# Compiles the user scout
##
def compileScout(logger):
    # 1. Set the target flags
    compiler = setTargetFlags(logger)

    # 2. Add additional flags:
    #  * flag_instructions - Will use the TCP server for instructions
    #  * flag_dynamic_buffers - Will use dynamic buffers (malloc) for the received instructions
    #  * flag_proxy - Will act as a proxy scout, only passing on the instructions to the driver
    compiler.setScoutFlags([flag_instructions, flag_dynamic_buffers, flag_proxy])

    # 3. Add custom compilation flags (not needed)
    # compiler.addCompilationFlags(compile_flags=[], link_flags=[])

    # 4. Compile the PC (user mode proxy) scout
    logger.info('Starting to compile the user scout')
    compiler.compile(scout_all_files, project_files, USER_SCOUT_BIN)
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
def main(args):
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
