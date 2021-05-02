class targetArc:
    """A class representing a target CPU architecture to which we will compile our binary.

    Attributes
    ----------
        compiler_path (str): path to the used compiler
        linker_path (str): path to the used linker
        objcopy_path (str): path to the used objcopy
        objcopy_flags (list): list of flags to be used by objcopy
        compile_flags (list): list of compilation flags
        link_flags (list): list of linking flags

    Notes
    -----
        Serves as a base class that will be extended by specific architecture classes.
    """

    native_compiler_path = 'gcc'
    native_linker_path   = 'ld'
    native_objcopy_path  = 'objcopy'
    native_objcopy_flags = ()

    base_compile_flags            = ('fno-builtin', 'Wno-int-to-pointer-cast', 'Wno-pointer-to-int-cast')
    base_executable_compile_flags = ('O2',)
    base_pic_compile_flags        = ('Os', 'nostdlib', 'fno-toplevel-reorder')
    base_link_flags               = ()

    def __init__(self, is_pic):
        """Init the base compilation configuration for the architecture.

        Args:
            is_pic (bool): True iff a position-independent compilation
        """
        self.compiler_path = self.native_compiler_path
        self.linker_path   = self.native_linker_path
        self.objcopy_path  = self.native_objcopy_path
        self.objcopy_flags = list(self.native_objcopy_flags)

        self.compile_flags = list(self.base_compile_flags)
        self.link_flags    = list(self.base_link_flags)

        self.compile_flags += self.base_pic_compile_flags if is_pic else self.base_executable_compile_flags

    def setToolchain(self, compiler_path, linker_path, objcopy_path, objcopy_flags):
        """Set the toolchain configurations for the given architecture.

        Args:
            compiler_path (str): path to the target compiler
            linker_path (str): path to the target linker
            objcopy_path (str): path to the target objcopy
            objcopy_flags (list): list of flags to be passed to objcopy
        """
        self.compiler_path = compiler_path
        self.linker_path   = linker_path
        self.objcopy_path  = objcopy_path
        self.objcopy_flags = [] + objcopy_flags

    def setNotNative(self):
        """Mark the compilation as using a toolchain and not the native compiler."""
        raise NotImplementedError("Subclasses should implement this!")

    def setEndianness(self, is_little):
        """Set the (little/big) endianness we are going to use.

        Args:
            is_little (bool): True iff compiling a Little Endian binary
        """
        raise NotImplementedError("Subclasses should implement this!")

    def setBitness(self, is_32_bits):
        """Set the (32/64) bitness we are going to use.

        Args:
            is_32_bits (bool): True iff compiling a 32-bits binary
        """
        raise NotImplementedError("Subclasses should implement this!")

    def prepareFlags(self):
        """Prepare the compilation and linking flags to be passed on to the compiler."""
        compile_flags = ' '.join(['-' + x for x in self.compile_flags])
        link_flags    = ' '.join(['-' + x for x in self.link_flags])
        return compile_flags, link_flags
