import os
import sys
import time
import struct

from .compilation.scout_flags import *
from .compilation.scout_files import *
from .compilation.arc_intel   import arcIntel
from .compilation.arc_arm     import arcArm, arcArmThumb
from .compilation.arc_mips    import arcMips

###################################
##  Architecture Configurations  ##
###################################

# Using an enum to support feature extensions
ARC_INTEL     = arcIntel.name()
ARC_ARM       = arcArm.name()
ARC_ARM_THUMB = arcArmThumb.name()
ARC_MIPS      = arcMips.name()

arc_factory = {
                ARC_INTEL:     arcIntel,
                ARC_ARM:       arcArm,
                ARC_ARM_THUMB: arcArmThumb,
                ARC_MIPS:      arcMips,
              }
              
arc_flags = {
                ARC_INTEL:     (flag_arc_intel,),
                ARC_ARM:       (flag_arc_arm,),
                ARC_ARM_THUMB: (flag_arc_arm, flag_arc_thumb),
                ARC_MIPS:      (flag_arc_mips,),
            }
            
#################
##  Utilities  ##
#################
            
def systemLine(line, logger):
        """Issues (and debug trace) a systen line

        Args:
            logger (logger, elementals): logger to be used by the function (elementals)
            line (string): cmd line to be executed
        """
        logger.debug(line)
        os.system(line)
        
###############################
##  The full Scout Compiler  ##
###############################

class scoutCompiler:
    def __init__(self, logger):
        self.logger = logger
        self.target_arc = None
        self.project_folder = None
        self.scout_folder = None
        self.config_flags = []        
        
    def setArc(self, arc, is_pic, is_32_bits=True, is_little_endian=True, is_native=False):
        """Sets the target's architecture specifications

        Args:
            arc (string, enum): name of the target architecture (should be a key of arc_factory)
            is_pic (bool): True iff compiling a position independent blob
            is_32_bits (bool, optional): True iff the architecture is 32 bit, otherwise it will be 64 bits (True by default)
            is_little_endian (bool, optional): True iff the architecture is little endian, otherwise it will be big endian (True by default)
            is_native (bool, optional): True iff should use the native compilation programs, regardless of the arc (False by default)
        """
        # Sanity check
        if arc not in arc_factory.keys():
            self.logger.error("Unknown architecture: \"%s\". Supported options are: \"%s\"", arc, ', '.join(arc_factory.keys()))

        # Apply the chosen settings
        self.target_arc = arc_factory[arc](is_pic)
        if not is_native:
            target_arc.setNotNative()
            
        # Configure the architecture
        target_arc.setEndianness(is_little_endian)
        target_arc.setBitness(is_32_bits)

        # Store the values for the configuration flags
        self.config_flags.append(flag_32_bit        if is_32_bits       else flag_64_bit)
        self.config_flags.append(flag_little_endian if is_little_endian else flag_big_endian)
        if is_pic:
            self.config_flags.append(flag_pic_code)

    def setScoutMode(self, is_user):
        """Sets the target's permission level

        Args:
            is_user (bool): True iff the scout will run in user mode, otherwise it will assume kernel mode permissions
        """
        self.config_flags.append(flag_mode_user if is_user else flag_mode_kernel)

    def setWorkingDirs(self, project_dir, scout_dir, include_dirs=[]):
        """Sets the paths for the used directories

        Args:
            project_dir (string): path to the project's directory
            scout_dir (string): path to the directory of the basic Scout (Example: ".../src/scout")
            include_dirs (list, optional): list of additional include directories
        """
        self.project_folder = project_dir
        self.scout_folder   = scout_dir

        # Ends with "/scout" (and not "/scout/")
        if scout_dir.endswith(os.path.sep + "scout"):
            main_folder = os.path.sep.join(scout_dir.split(os.path.sep)[:-1])
        else:
            main_folder = scout_dir + os.path.sep + ".."

        self.target_arc.compile_flags += ['I' + x for x in [project_folder, main_folder] + include_dirs]
    
    def addScoutFlags(self, flags):
        """Adds the flags regarding the target's specifications

        Args:
            flags (list): list of configuration flags (strings)
        """
        self.config_flags += flags
    
    def addCompilationFlags(self, user_compile_flags=[], user_link_flags=[]):
        """Add custom compilation / linking flags

        Args:
            user_compile_flags (list, optional): list of compiler flags (without the '-' prefix)
            user_link_flags (list, optional) list of linker flags (without the '-' prefix)
        """    
        self.target_arc.compile_flags += user_compile_flags
        self.target_arc.link_flags    += user_link_flags

    def verifyScoutFlags(self):
        """Checks that all of the configuration flags are set correctly"""
        if flag_mode_user is not in self.config_flags and flag_mode_kernel is not in self.config_files:
            self.logger.warning("Missing Scout flag - unknown permission mode. Defaulting to USER-MODE (low privileges)")

    def generateFlagsFile(self):
        """Generates the architecture's "flags.h" file"""
        # Verify the flags
        verifyScoutFlags()

        # Verify we know where to store this file
        if self.project_folder is None:
            self.logger.error("Working directories are NOT defined...")
            return

        flag_path = os.path.join(self.project_folder, FLAGS_FILE_NAME)
        self.logger.info(f"Generating the {flag_path} file")
        fd = open(flag_path, "w")
        # file prefix
        fd.write("#ifndef __SCOUT__FLAGS__H__\n")
        fd.write("#define __SCOUT__FLAGS__H__\n")
        fd.write('\n')
        # auto-generation comment
        fd.write("/* This file is AUTO-GENERATED, please do NOT edit it manually */\n")
        # The actual flags
        for flag in self.config_flags:
            fd.write(f"#define {flag}\n")
        # file suffix
        fd.write("\n")
        fd.write("#endif /* _SCOUT__FLAGS__H__ */")
        # can close the file
        fd.close()

    def compilePICScout(self, scout_files, project_files, elf_file, final_file):
        """Compiles a Position-Independent (PIC) "Scout" project

        Args:
            scout_files (list): list of file paths for scout's code (*.c) files
            proect_files (list): list of file paths for the project's code (*.c) files
            elf_file (string): path to the (created) compiled ELF file
            final_file (string): path to the (created) PIC binary file
        """
        self.logger.addIndent()

        # 0. Sanity check
        if flag_pic_code not in self.config_flags:
            self.logger.error("Compiling a PIC scout without the PIC-CODE Environment flag. Did you mean: compileExecutableScout() ?")
            self.logger.removeIndent()
            return

        # 1. Auto-Generate the flags.h file
        generateFlagsFile()
        
        # 2. Prepare the list of compilation files        
        compilation_files = [os.path.join(self.scout_folder, f) for f in scout_files] + project_files

        # 3. Generate all of the *.S files
        self.logger.info("Compiling the *.c files")
        compile_flags, link_flags = self.target_arc.prepareFlags()
        s_files = []
        for c_file in compilation_files:
            local_out_file = ".".join(c_file.split(".")[:-1]) + ".S"
            systemLine(f"{target_arc.compiler_path} -S -c {compile_flags} {c_file} -o {local_out_file}", self.logger)
            s_files.append(local_out_file)

        # 4. Work-around GCC's bugs
        self.logger.info("Fixing the *.S files to work around GCC's bugs")
        for s_file in s_files:
            fd = open(s_file, "r")
            content = fd.read()
            fd.close()
            content = content.replace(".space #", ".space ").replace(".space $", ".space ")
            # Mips: convert the calls to relative (PIC)
            if self.target_arc.name() == arcMips.name():
                content = content.replace("\tjal\t", "\tbal\t").replace("\tj\t", "\tb\t")
            fd = open(s_file, "w")
            fd.write(content)
            fd.close()

        # 5. Generate all of the *.o files
        self.logger.info("Compiling the *.S files")
        o_files = []
        for s_file in s_files:
            local_out_file = ".".join(s_file.split(".")[:-1]) + ".o"
            systemLine(f"{target_arc.compiler_path} -c {compile_flags} {s_file} -o {local_out_file}", self.logger)
            o_files.append(local_out_file)

        # 6. Link together all of the *.o files
        self.logger.info(f"Linking together all of the files, creating: {elf_file}")
        systemLine(f"{target_arc.linker_path} {link_flags} {' '.join(o_files)} -o {elf_file}", self.logger)

        # 7. Objcopy the content to the actual wanted file
        self.logger.info(f"Extracting the final binary to: {final_file}")
        systemLine(f"{target_arc.objcopy_path} -O binary -j .text -j .rodata {' '.join(target_arc.objcopy_flags)} {elf_file} {final_file}", self.logger)

        self.logger.removeIndent()

    def compileExecutableScout(self, scout_files, project_files, elf_file):
        """Compiles a regular executable "Scout" project

        Args:
            scout_files (list): list of file paths for scout's code (*.c) files
            proect_files (list): list of file paths for the project's code (*.c) files
            elf_file (string): path to the (created) compiled ELF file
        """
        # 0. Sanity check
        if flag_pic_code in self.config_flags:
            logger.error("Compiling an Executable scout with PIC-CODE environment flag. Did you mean: compilePICScout() ?")
            return

        # 1. Auto-Generate the flags.h file
        generateFlagsFile()

        # 2. Re-organize the linker flags
        compile_flags, link_flags = self.target_arc.prepareFlags()
        fixed_link_flags = "".join("-Wl," + x for x in link_flags.split("-")[1:])
        
        # 3. Prepare the list of compilation files
        compilation_files = [os.path.join(self.scout_folder, f) for f in scout_files] + project_files

        # 4. Compile together all of the file (and that's it)
        self.logger.info(f"Compiling the *.c files, linking them together and creating: {elf_file}")
        systemLine(f"{target_arc.compiler_path} {compile_flags} {' '.join(compilation_files)} {fixed_link_flags} -o {elf_file}", self.logger)