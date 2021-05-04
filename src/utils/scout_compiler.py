import os
import struct

from .compilation.scout_flags import *
from .compilation.scout_files import *
from .compilation.arc_intel   import arcIntel
from .compilation.arc_arm     import arcArm, arcArmThumb
from .compilation.arc_mips    import arcMips
from .context_creator         import *

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
    """Issue (and debug trace) a systen line.

    Args:
        line (string): cmd line to be executed
        logger (logger, elementals): logger to be used by the function (elementals)
    """
    logger.debug(line)
    os.system(line)

###############################
##  The full Scout Compiler  ##
###############################

class scoutCompiler:
    """A class representing the Scout Compiler object, which manages the entire compilation logic.

    Attributes
    ----------
        logger (logger): (elementals) logger
        target_arc (targetArc): target architecture instance to hold CPU-specific configurations
        project_folder (str): path to the user's working folder
        scout_folder (str): path to Scout's base folder
        config_flags (list): list of Scout configuration flags, accumulated along the process
        is_32_bits (bool): True iff we are going to compile a 32-bits binary
        is_little_endian (bool): True iff we are going to compile a Little Endian binary
        is_pic (bool): True iff we are going to compile a PIC binary blob
        full_got (bytes): blob containing the GOT function address table for a PIC compilation
        global_vars (bytes): blob containing the global variables content for a PIC compilation

    Notes
    -----
        This class serves as the main object to be used by the suer when compiling an executable or
        a Position-Independent-Code (PIC) Scout binary.
    """

    def __init__(self, logger):
        """Construct the basic Scout compiler object.

        Args:
            logger (logger): (elementals) logger
        """
        self.logger = logger
        self.target_arc = None
        self.project_folder = None
        self.scout_folder = None
        self.config_flags = []
        self.is_32_bits = True
        self.is_little_endian = True
        self.is_pic = False
        self.full_got = b''
        self.global_vars = b''

    def setArc(self, arc, is_pic, is_32_bits=True, is_little_endian=True, is_native=False):
        """Set the target's architecture specifications.

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
        self.is_pic = is_pic
        self.target_arc = arc_factory[arc](is_pic)
        if is_native:
            self.config_flags.append(flag_native_compiler)
        else:
            self.target_arc.setNotNative()

        # Configure the architecture
        self.target_arc.setEndianness(is_little_endian)
        self.target_arc.setBitness(is_32_bits)
        self.is_32_bits = is_32_bits
        self.is_little_endian = is_little_endian

        # Store the values for the configuration flags
        self.config_flags.append(flag_32_bit        if is_32_bits       else flag_64_bit)
        self.config_flags.append(flag_little_endian if is_little_endian else flag_big_endian)
        self.config_flags += list(arc_flags[arc])
        if self.is_pic:
            self.config_flags.append(flag_pic_code)

    def setScoutMode(self, is_user):
        """Set the target's permission level.

        Args:
            is_user (bool): True iff the scout will run in user mode, otherwise it will assume kernel mode permissions
        """
        self.config_flags.append(flag_mode_user if is_user else flag_mode_kernel)

    def setWorkingDirs(self, project_dir, scout_dir, include_dirs=[]):
        """Set the paths for the used directories.

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

        self.target_arc.compile_flags += ['I' + x for x in [self.project_folder, main_folder] + include_dirs]

    def addScoutFlags(self, flags):
        """Add the flags regarding the target's specifications.

        Args:
            flags (list): list of configuration flags (strings)
        """
        self.config_flags += flags

    def addCompilationFlags(self, user_compile_flags=[], user_link_flags=[]):
        """Add custom compilation / linking flags.

        Args:
            user_compile_flags (list, optional): list of compiler flags (without the '-' prefix)
            user_link_flags (list, optional) list of linker flags (without the '-' prefix)
        """
        self.target_arc.compile_flags += user_compile_flags
        self.target_arc.link_flags    += user_link_flags

    def verifyScoutFlags(self):
        """Check that all of the configuration flags are set correctly."""
        if flag_mode_user not in self.config_flags and flag_mode_kernel not in self.config_files:
            self.logger.warning("Missing Scout flag - unknown permission mode. Defaulting to USER-MODE (low privileges)")

    def generateFlagsFile(self):
        """Generate the architecture's "flags.h" file."""
        # Verify the flags
        self.verifyScoutFlags()

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

    def populateGOT(self, scout_got, project_got, project_vars_size=0, is_host_thumb=False):
        """Populate the PIC context with the GOT entries, and capacity for global variables.

        Args:
            scout_got (list): list of (virtual) addresses according to Scout's GOT order
            project_got (list): list of additional memory addresses for symbols used in the project's GOT
            projects_vars_size (int, optional): size (in bytes) of the project's global variables (0 by default)
            is_host_thumb (bool, optional): True iff the host process is a Thumb binary (False by default)
        """
        # Sanity Check #1 - PIC Compilation
        if not self.is_pic:
            self.logger.error("Can't populate a PIC context (GOT and globals) for a non-PIC compilation!")
            return

        # Sanity Check #2 - GOT Size
        expected_size = scout_got_base_size_mmap if flag_mmap in self.config_flags else scout_got_base_size
        if len(scout_got) != expected_size:
            self.logger.error(f"Wrong size for Scout's GOT: Expected {expected_size} entries, and got {len(scout_got)}!")
            return

        format = ("<" if self.is_little_endian else ">") + ("L" if self.is_32_bits else "Q")
        self.full_got = b''.join([struct.pack(format, func + (1 if is_host_thumb else 0)) for func in scout_got + project_got])

        # Calculate the size for the global variables
        size_globals = project_vars_size
        # The base loaders don't use global variables, only the full scout
        if flag_loader not in self.config_flags:
            if flag_instructions in self.config_flags:
                if self.is_32_bits:
                    size_globals += scout_instructions_globals_32_size
                    if flag_dynamic_buffers not in self.config_flags:
                        size_globals += scout_static_buffers_32_size
                else:
                    size_globals += scout_instructions_globals_64_size
                    if flag_dynamic_buffers not in self.config_flags:
                        size_globals += scout_static_buffers_64_size
        # Now generate the blob
        self.global_vars = b'\x00' * size_globals

    def compile(self, scout_files, project_files, elf_file):
        """Compile the "Scout" project, according to the PIC setup that was defined earlier.

        Args:
            scout_files (list): list of file paths for scout's code (*.c) files
            proect_files (list): list of file paths for the project's code (*.c) files
            elf_file (string): path to the (created) compiled ELF file

        Note:
            If this is a PIC compilation, the final binary file will be named to match the ELF
            file. For example: "project.elf" => "project.bin".

        Return Value:
            Name of the PIC binary file (in PIC compilations), None otherwise.
        """
        self.logger.addIndent()
        # 1. Auto-Generate the flags.h file
        self.generateFlagsFile()

        # 2. Prepare the list of compilation files
        compilation_files = [os.path.join(self.scout_folder, f) for f in scout_files] + project_files

        # 3. Prepare the compilation & linking flags
        compile_flags, link_flags = self.target_arc.prepareFlags()

        #############################
        ## Compiling an Executable ##
        #############################

        if not self.is_pic:
            # 4. Re-organize the linker flags
            fixed_link_flags = "".join("-Wl,-" + x for x in link_flags.split("-")[1:])

            # 5. Compile together all of the file (and that's it)
            self.logger.info(f"Compiling the *.c files, linking them together and creating: {elf_file}")
            systemLine(f"{self.target_arc.compiler_path} {compile_flags} {' '.join(compilation_files)} {fixed_link_flags} -o {elf_file}", self.logger)

            self.logger.removeIndent()
            return None

        ###########################
        ## Compiling a PIC Scout ##
        ###########################

        # 4. Generate all of the *.S files
        self.logger.info("Compiling the *.c files")
        compile_flags, link_flags = self.target_arc.prepareFlags()
        s_files = []
        for c_file in compilation_files:
            local_out_file = ".".join(c_file.split(".")[:-1]) + ".S"
            systemLine(f"{self.target_arc.compiler_path} -S -c {compile_flags} {c_file} -o {local_out_file}", self.logger)
            s_files.append(local_out_file)

        # 5. Work-around GCC's bugs
        # We can afford these changes due to the following:
        # a) We only perform them on PIC compilations
        # b) PIC compilations don't contain string literals, so we won't conflict with them
        # c) Our strings are very specific, so they (probably) won't conflict with something else
        self.logger.info("Fixing the *.S files to work around GCC's bugs")
        for s_file in s_files:
            fd = open(s_file, "r")
            content_lines = fd.readlines()
            fd.close()

            new_content_lines = []
            for content in content_lines:
                # Makes sure that only our special "_start" will be at the beginning of the compiled blob
                # This is needed because gcc tends to place "Main" in .text.startup section, instead of our _start.
                if ".section	.text.startup" in content and "Scout" not in content:
                    continue
                content = content.replace(".space #", ".space ").replace(".space $", ".space ")
                # Mips: convert the calls to relative (PIC)
                if self.target_arc.name() == ARC_MIPS:
                    content = content.replace("\tjal\t", "\tbal\t").replace("\tj\t", "\tb\t")
                # save the modified line
                new_content_lines.append(content)

            fd = open(s_file, "w")
            fd.writelines(new_content_lines)
            fd.close()

        # 6. Generate all of the *.o files
        self.logger.info("Compiling the *.S files")
        o_files = []
        for s_file in s_files:
            local_out_file = ".".join(s_file.split(".")[:-1]) + ".o"
            systemLine(f"{self.target_arc.compiler_path} -c {compile_flags} {s_file} -o {local_out_file}", self.logger)
            o_files.append(local_out_file)

        # 7. Link together all of the *.o files
        self.logger.info(f"Linking together all of the files, creating: {elf_file}")
        systemLine(f"{self.target_arc.linker_path} {link_flags} {' '.join(o_files)} -o {elf_file}", self.logger)

        # 8. Objcopy the content to the actual wanted file
        if elf_file.split('.')[-1].lower() == "elf":
            binary_file = '.'.join(elf_file.split('.')[:-1] + ['bin'])
        else:
            binary_file = elf_file + ".bin"
        self.logger.info(f"Extracting the final binary to: {binary_file}")
        systemLine(f"{self.target_arc.objcopy_path} -O binary -j .text -j .rodata {' '.join(self.target_arc.objcopy_flags)} {elf_file} {binary_file}", self.logger)

        # 9. Place the PIC context inside the file
        placeContext(self.full_got, self.global_vars, binary_file, self.logger)

        self.logger.removeIndent()
        return binary_file
