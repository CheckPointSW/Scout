import os
import sys
import time
import struct

##############################
##  Default Configurations  ##
##############################

# Native Compiler
native_compiler_path = 'gcc'
native_linker_path   = 'ld'
native_objcopy_path  = 'objcopy'

# Arm Compiler
arm_compiler_path   = '/usr/bin/arm-none-eabi-gcc'
arm_linker_path     = '/usr/bin/arm-none-eabi-ld'
arm_objcopy_path    = '/usr/bin/arm-none-eabi-objcopy'
arm_objcopy_flags   = ['--section-alignment 4']

# Mips Compiler
mips_compiler_path   = '/usr/bin/mips-linux-gnu-gcc'
mips_linker_path     = '/usr/bin/mips-linux-gnu-ld'
mips_objcopy_path    = '/usr/bin/mips-linux-gnu-objcopy'
mips_objcopy_flags   = ['--section-alignment 4']

# Intel Compiler
intel_compiler_path = 'gcc'
intel_linker_path   = 'ld'
intel_objcopy_path  = 'objcopy'
intel_objcopy_flags = []

# Compile & Link flags
common_compile_flags            = ['fno-builtin', 'Wno-int-to-pointer-cast', 'Wno-pointer-to-int-cast']
common_executable_compile_flags = ['O2']
common_pic_compile_flags        = ['Os', 'nostdlib', 'fno-toplevel-reorder']
intel_pic_compile_flags         = []
arm_pic_compile_flags           = ['fno-jump-tables', 'mapcs-frame']
mips_pic_compile_flags          = ['fno-jump-tables', 'mno-shared', 'mplt']
common_link_flags               = []

#############################
##  Static Configurations  ##
#############################

# flags files
FLAGS_FILE_NAME     = 'flags.h'

# configuration compile flags
flag_32_bit         = 'SCOUT_BITS_32'
flag_64_bit         = 'SCOUT_BITS_64'
flag_big_endian     = 'SCOUT_BIG_ENDIAN'
flag_little_endian  = 'SCOUT_LITTLE_ENDIAN'
flag_arc_arm        = 'SCOUT_ARCH_ARM'
flag_arc_mips       = 'SCOUT_ARCH_MIPS'
flag_arc_intel      = 'SCOUT_ARCH_INTEL'
flag_arc_thumb      = 'SCOUT_ARM_THUMB'
flag_mode_user      = 'SCOUT_MODE_USER'
flag_mode_kernel    = 'SCOUT_MODE_KERNEL'
flag_pic_code       = 'SCOUT_PIC_CODE'
flag_instructions   = 'SCOUT_INSTRUCTIONS'
flag_restore_flow   = 'SCOUT_RESTORE_FLOW'
flag_dynamic_buffers= 'SCOUT_DYNAMIC_BUFFERS'
flag_proxy          = 'SCOUT_PROXY'
flag_mmap           = 'SCOUT_MMAP'
flag_load_thumb     = 'SCOUT_LOADING_THUMB_CODE'
flag_loader         = 'SCOUT_LOADER'

# Using an enum to support feature extensions
ARC_INTEL = 'intel'
ARC_ARM   = 'arm'
ARC_MIPS  = 'mips'

arc_setups = {
                ARC_INTEL:  (intel_compiler_path, intel_linker_path, intel_objcopy_path, intel_objcopy_flags),
                ARC_ARM:    (arm_compiler_path, arm_linker_path, arm_objcopy_path, arm_objcopy_flags),
                ARC_MIPS:   (mips_compiler_path, mips_linker_path, mips_objcopy_path, mips_objcopy_flags),
             }
arc_configs = {
                ARC_INTEL:  flag_arc_intel,
                ARC_ARM:    flag_arc_arm,
                ARC_MIPS:   flag_arc_mips,
              }
              
arc_pic_flags = \
              {
                ARC_INTEL:  intel_pic_compile_flags,
                ARC_ARM:    arm_pic_compile_flags,
                ARC_MIPS:   mips_pic_compile_flags,
              }

# scout file list
scout_arc_files     = ['arc/arm.c', 'arc/mips.c', 'arc/intel.c']
scout_pic_files     = ['pic/arm_pic_wrapper.c', 'pic/mips_pic_wrapper.c', 'pic/intel_pic_wrapper.c', 'pic/scout_plt.c', 'pic/scout_globals.c']
scout_server_loader = 'loaders/tcp_server_loader.c'
scout_client_loader = 'loaders/tcp_client_loader.c'
scout_loader_deps   = scout_pic_files + ['pack.c', 'tcp_server.c'] + scout_arc_files
scout_all_files     = scout_pic_files + ['pack.c', 'scout_api.c', 'tcp_server.c'] + scout_arc_files

########################
##  Global Variables  ##
########################

# User compiler & linker
compiler_path       = None
linker_path         = None
objcopy_path        = None
objcopy_flags       = None

# Scout configurations flags
config_bitness      = None
config_endianness   = None
config_arc          = None
config_mode         = None
config_pic          = None
config_flags        = []

# Paths
project_folder      = None
scout_folder        = None
include_dirs        = None

def setScoutArc(arc, is_32_bits, is_little_endian, logger, is_native=False):
    """Sets the target's architecture specifications

    Args:
        arc (string, enum): name of the target architecture (should be a key of arc_setups)
        is_32_bits (bool): True iff the architecture is 32 bit, otherwise it will be 64 bits
        is_little_endian (bool): True iff the architecture is little endian, otherwise it will be big endian
        logger (logger): (elementals) logger
        is_native (bool, optional): True iff should use the native compilation programs, regardless of the arc (False by default)
    """
    global compiler_path, linker_path, objcopy_path, objcopy_flags, config_bitness, config_endianness, config_arc

    # Sanity check
    if arc not in arc_setups.keys():
        logger.error("Unknown architecture: \"%s\". Supported options are: \"%s\"", arc, ', '.join(arc_setups.keys()))

    # Apply the chosen settings
    compiler_path, linker_path, objcopy_path, objcopy_flags = arc_setups[arc]
    if is_native:
        compiler_path = native_compiler_path
        linker_path   = native_linker_path
        objcopy_path  = native_objcopy_path

    # Store the values for the configuration flags
    config_bitness      = flag_32_bit           if is_32_bits       else flag_64_bit
    config_endianness   = flag_little_endian    if is_little_endian else flag_big_endian
    config_arc          = arc_configs[arc]

def setScoutEnv(is_executable):
    """Sets the target's environment flags

    Args:
        is_executable (bool): True iff the environment is a standard executable, otherwise it will be a PIC environment
    """
    global config_pic

    config_pic = flag_pic_code if not is_executable else ''

def setScoutMode(is_user):
    """Sets the target's permission level

    Args:
        is_user (bool): True iff the scout will run in user mode, otherwise it will assume kernel mode permissions
    """
    global config_mode

    config_mode = flag_mode_user if is_user else flag_mode_kernel

def setScoutFlags(flags):
    """Sets the flags regarding the target's specifications

    Args:
        flags (list): list of configuration flags (strings)
    """
    global config_flags

    config_flags = [] + flags

def setWorkingDirs(project_dir, scout_dir):
    """Sets the paths for the used directories

    Args:
        project_dir (string): path to the project's directory
        scout_dir (string): path to the directory of the basic Scout
    """
    global project_folder, scout_folder, include_dirs

    project_folder = project_dir
    scout_folder   = scout_dir

    if scout_folder.endswith(os.path.sep + "scout"):
        main_folder = os.path.sep.join(scout_folder.split(os.path.sep)[:-1])
    else:
        main_folder = scout_folder + os.path.sep + ".."

    # Can update the include directories
    include_dirs = [project_folder, main_folder]

def addIncludeDirs(dirs):
    """Adds additional include directories for the compilation

    Args:
        dirs (list): list of additional include directories
    """
    global include_dirs

    include_dirs += dirs

def verifyScoutFlags(logger):
    """Checks that all of the configuration flags are set correctly

    Args:
        logger (logger): (elementals) logger

    Return Value:
        True iff all configuration flags are set to a valid value, False otherwise
    """
    global config_flags

    if config_bitness is None:
        logger.error("Missing Scout flag: unknown bitness")
        return False

    if config_endianness is None:
        logger.error("Missing Scout flag: unknown endianness")
        return False

    if config_arc is None:
        logger.error("Missing Scout flag: unknown architecture")
        return False

    if config_mode is None:
        logger.error("Missing Scout flag: unknown permission mode")
        return False

    if config_pic is None:
        logger.error("Missing Scout flag: should decide if compiling in PIC mode")
        return False

    # Reaching here means that all was OK
    config_flags  += [config_bitness, config_endianness, config_arc, config_mode]
    if len(config_pic) > 0:
        config_flags += [config_pic]
    return True

def generateFlagsFile(logger):
    """Generates the architecture's "flags.h" file

    Args:
        logger (logger): (elementals) logger
    """
    # Verify the flags
    if not verifyScoutFlags(logger):
        return

    # Verify we know where to store this file
    if project_folder is None:
        logger.error("Working directories are NOT defined...")
        return

    flag_path = os.path.join(project_folder, FLAGS_FILE_NAME)
    logger.info(f"Generating the {flag_path} file")
    fd = open(flag_path, "w")
    # file prefix
    fd.write("#ifndef __SCOUT__FLAGS__H__\n")
    fd.write("#define __SCOUT__FLAGS__H__\n")
    fd.write('\n')
    # auto-generation comment
    fd.write("/* This file is AUTO-GENERATED, please do NOT edit it manually */\n")
    # The actual flags
    for flag in set(config_flags):
        fd.write(f"#define {flag}\n")
    # file suffix
    fd.write("\n")
    fd.write("#endif /* _SCOUT__FLAGS__H__ */")
    # can close the file
    fd.close()

def generateCompilationFlags(user_compile_flags, user_link_flags, logger):
    """Generates the compilation flags that match the configurations flags

    Args:
        user_copmile_flags (list): list of compiler flags (without the '-' prefix)
        user_link_flags (list) list of linker flags (without the '-' prefix)
        logger (logger): (elementals) logger

    Return Value:
        (compiler flags string, linker flags string)
    """
    compile_flags  = common_compile_flags
    link_flags     = common_link_flags

    # ARM - Misc (Thumb) & Endianness
    if config_arc == flag_arc_arm:
        # Thumb
        compile_flags     += ['mthumb'] if (flag_arc_thumb in config_flags) else []
        # Endianness
        if config_endianness == flag_little_endian:
            compile_flags += ['mlittle-endian']
            link_flags    += ['EL']
        else:
            compile_flags += ['mbig-endian']
            link_flags    += ['EB']

    # Mips - Endianness
    elif config_arc == flag_arc_mips:
        if config_endianness == flag_little_endian:
            compile_flags += ['EL']
            link_flags    += ['EL']
        else:
            compile_flags += ['EB']
            link_flags    += ['EB']
            
    # Intel - Misc (Bitness)
    elif config_arc == flag_arc_intel:
        if config_bitness == flag_32_bit:
            compile_flags += ['m32']
            link_flags    += ['melf_i386']

    # Executable Environment
    if config_pic != flag_pic_code:
        compile_flags += common_executable_compile_flags

    # PIC Environment
    else:
        compile_flags += common_pic_compile_flags
        compile_flags += arc_pic_flags[config_arc]

    # Final Compile & Link flags
    compile_flags = ' '.join(['-' + x for x in compile_flags + user_compile_flags + ['I' + y for y in include_dirs]])
    link_flags    = ' '.join(['-' + x for x in link_flags + user_link_flags])

    return compile_flags, link_flags

def systemLine(line, logger):
    """Issues and debug trace a systen line

    Args:
        line (string): cmd line to be executed
        logger (logger): (elementals) logger
    """
    logger.debug(line)
    os.system(line)

def compilePICScout(compilation_files, compile_flags, link_flags, elf_file, final_file, logger):
    """Compiles a Position-Independent (PIC) "Scout" project

    Args:
        compilation_files (list): list of file paths for all code (*.c) files
        compile_flags (string): compilation flags to be passed to the compiler
        link_flags (string): linker flags to be passed to the linker
        elf_file (string): path to the (created) compiled ELF file
        final_file (string): path to the (created) PIC binary file
        logger (logger): (elementals) logger
    """
    logger.addIndent()

    # 0. Sanity check
    if config_pic != flag_pic_code:
        logger.error("Compiling a PIC scout without the PIC-CODE Environment flag. Did you mean: compileExecutableScout() ?")
        logger.removeIndent()
        return

    # 1. Auto-Generate the flags.h file
    generateFlagsFile(logger)

    # 2. Generate all of the *.S files
    logger.info("Compiling the *.c files")
    s_files = []
    for c_file in compilation_files:
        local_out_file = ".".join(c_file.split(".")[:-1]) + ".S"
        systemLine(f"{compiler_path} -S -c {compile_flags} {c_file} -o {local_out_file}", logger)
        s_files.append(local_out_file)

    # 3. Work-around GCC's bugs
    logger.info("Fixing the *.S files to work around GCC's bugs")
    for s_file in s_files:
        fd = open(s_file, "r")
        content = fd.read()
        fd.close()
        content = content.replace(".space #", ".space ").replace(".space $", ".space ")
        # convert the calls to relative (PIC)
        if config_arc == flag_arc_mips:
            content = content.replace("\tjal\t", "\tbal\t").replace("\tj\t", "\tb\t")
        fd = open(s_file, "w")
        fd.write(content)
        fd.close()

    # 4. Generate all of the *.o files
    logger.info("Compiling the *.S files")
    o_files = []
    for s_file in s_files:
        local_out_file = ".".join(s_file.split(".")[:-1]) + ".o"
        systemLine(f"{compiler_path} -c {compile_flags} {s_file} -o {local_out_file}", logger)
        o_files.append(local_out_file)

    # 5. Link together all of the *.o files
    logger.info(f"Linking together all of the files, creating: {elf_file}")
    systemLine(f"{linker_path} {link_flags} {' '.join(o_files)} -o {elf_file}", logger)

    # 6. Objcopy the content to the actual wanted file
    logger.info(f"Extracting the final binary to: {final_file}")
    systemLine(f"{objcopy_path} -O binary -j .text -j .rodata {' '.join(objcopy_flags)} {elf_file} {final_file}", logger)

    logger.removeIndent()

def compileExecutableScout(compilation_files, compile_flags, link_flags, elf_file, logger):
    """Compiles a regular executable "Scout" project

    Args:
        compilation_files (list): list of file paths for all code (*.c) files
        compile_flags (string): compilation flags to be passed to the compiler
        link_flags (string): linker flags to be passed to the linker
        elf_file (string): path to the (created) compiled ELF file
        logger (logger): (elementals) logger
    """
    # 0. Sanity check
    if config_pic == flag_pic_code:
        logger.error("Compiling an Executable scout with PIC-CODE environment flag. Did you mean: compilePICScout() ?")
        return

    # 1. Auto-Generate the flags.h file
    generateFlagsFile(logger)

    # 2. Re-organize the linker flags
    fixed_link_flags = "".join("-Wl," + x for x in link_flags.split("-")[1:])

    # 3. Compile together all of the file (and that's it)
    logger.info(f"Compiling the *.c files, linking them together and creating: {elf_file}")
    systemLine(f"{compiler_path} {compile_flags} {' '.join(compilation_files)} {fixed_link_flags} -o {elf_file}", logger)
