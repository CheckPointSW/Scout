#!/usr/bin/python
import os
import sys
import time
import struct
from elementals import Prompter

from scout.scout_compiler  import *
from scout.context_creator import *

##############################
##  Dynamic Configurations  ##
##############################

SCOUT_DIR           = '../../../src/scout'

SCOUT_LOADER_ELF    = 'scout_loader.elf'
SCOUT_LOADER_BIN    = 'scout_loader.bin'

EMBEDDED_SCOUT_ELF  = 'embedded_scout.elf'
EMBEDDED_SCOUT_BIN  = 'embedded_scout.bin'

TARGET_ARCH         = ARC_ARM
# Is Little Endian
TARGET_ENDIANNESS   = True if TARGET_ARCH == ARC_INTEL else False
# Is 32 bits?
TARGET_BITNESS      = True if TARGET_ARCH != ARC_INTEL else False

# Scout Functions (in same order as the c code)
symbol_memcpy  		= 0x80486c0
symbol_memset  		= 0x8048770
symbol_malloc  		= 0x80486f0
symbol_free    		= 0x80486b0
symbol_socket  		= 0x80487b0
symbol_bind    		= 0x8048760
symbol_listen  		= 0x80487a0
symbol_accept  		= 0x80486e0
symbol_connect 		= 0x80487c0
symbol_recv    		= 0x80487d0
symbol_send    		= 0x80487f0
symbol_close   		= 0x80487e0
symbol_mmap    		= 0x8048740
symbol_mprotect		= 0x8048680
symbol_munmap  		= 0x8048790
# Loader Functions (none for now)
loader_got          = []
# Project Functions (none for now)
project_got         = []

# loader files list
loader_pic_files    = ['loader_plt.c', 'loader_globals.c']
# project files list
project_pic_files   = ['project_plt.c', 'project_globals.c']
project_files       = ['arm_scout.c', 'project_instructions.c'] + project_pic_files

##
# Sets the basic architecture flags for our target
##
def setTargetFlags(logger):
    # 0. Create the compiler instance
    compiler = scoutCompiler(logger)
    
    # 1. Set the architecture    
    compiler.setArc(TARGET_ARCH, is_pic=True, is_32_bits=TARGET_BITNESS, is_little_endian=TARGET_ENDIANNESS)

    # 2. Set the permission mode (User & low CPU permissions, Kernel & High CPU permissions)
    compiler.setScoutMode(is_user=True)
    
    # 3. Set the working directories
    compiler.setWorkingDirs(project_dir='.', scout_dir=SCOUT_DIR)
    
    return compiler

##
# Compiles the scout loader (TCP Server loader)
##
def compileScoutLoader(logger):
    # 1. Set the target flags
    compiler = setTargetFlags(logger)

    # 2. Additional flags:
    #  * flag_loader - Compiling a loader
    #  * flag_loader_server - Compiling a TCP server loader
    #  * flag_mmap - The loader will use mmap() instead of malloc()
    #  X flag_load_thumb - If will be loading a Thumb code full Scout
    #  X flag_loader_transmit - If the loader will need to be able to send TCP messages
    compiler.addScoutFlags([flag_loader, flag_loader_server, flag_mmap])

    # 3. Add custom compilation flags (not needed)
    # compiler.addCompilationFlags(compile_flags=[], link_flags=[])

    # 4. Compile an embedded scout
    logger.info('Starting to compile the scout loader')
    compiler.compilePICScout(scout_server_loader_deps, loader_pic_files, SCOUT_LOADER_ELF, SCOUT_LOADER_BIN)

    # 5. Place the PIC context in the resulting binary file
    generateGOT(symbol_memcpy, symbol_memset, symbol_malloc, symbol_free, symbol_socket, symbol_bind,
                symbol_listen, symbol_accept, symbol_connect, symbol_recv, symbol_send, symbol_close,
                symbol_mmap, symbol_mprotect, symbol_munmap, project_got=loader_got, is_thumb=TARGET_ARCH == ARC_ARM)

    # 6. Setup the sizes for the global variables (No variables used at all)
    generateGlobals(scout_vars_size=0, project_vars_size=0)

    # 7. Generate the PIC context, and place it in the binary blob
    placeContext(SCOUT_LOADER_BIN, SCOUT_LOADER_BIN, TARGET_ENDIANNESS, TARGET_BITNESS, logger)
    return

##
# Compiles the scout project
##
def compileScout(logger):
    # 1. Set the target flags
    compiler = setTargetFlags(logger)

    # 2. Add additional flags:
    #  * flag_instructions - Will use the TCP server for instructions
    #  * flag_dynamic_buffers - Will use dynamic buffers (malloc) for the received instructions
    compiler.addScoutFlags([flag_instructions, flag_dynamic_buffers])

    # 3. Add custom compilation flags (not needed)
    # compiler.addCompilationFlags(compile_flags=[], link_flags=[])

    # 4. Compile a PIC scout
    logger.info('Starting to compile the PIC scout')
    compiler.compilePICScout(scout_all_files, project_files, EMBEDDED_SCOUT_ELF, EMBEDDED_SCOUT_BIN, logger)

    # 5. Place the PIC context in the resulting binary file
    generateGOT(symbol_memcpy, symbol_memset, symbol_malloc, symbol_free, symbol_socket, symbol_bind,
                symbol_listen, symbol_accept, symbol_connect, symbol_recv, symbol_send, symbol_close,
                project_got=project_got)

    # 6. Setup the sizes for the global variables
    generateGlobals(scout_vars_size=scout_instructions_globals_32_size if TARGET_BITNESS else scout_instructions_globals_64_size, project_vars_size=0)

    # 7. Generate the PIC context, and place it in the binary blob
    placeContext(EMBEDDED_SCOUT_BIN, EMBEDDED_SCOUT_BIN, TARGET_ENDIANNESS, TARGET_BITNESS, logger)
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

    # Compile the scout's loader (TCP server)
    compileScoutLoader(prompter)
    # Compile the full scout
    compileScout(prompter)

    prompter.info('Finished Successfully')

if __name__ == '__main__':
    main(sys.argv)